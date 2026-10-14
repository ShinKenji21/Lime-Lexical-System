"""
LIME Lexical Analyzer
=====================

WHAT THIS FILE DOES
    It reads LIME source code one character at a time and splits it into
    TOKENS (the smallest meaningful pieces of the language: reserved words,
    identifiers, numbers, strings, symbols, comments).  Anything that does not
    form a valid token is reported as a LEXICAL ERROR instead.

HOW IT FOLLOWS THE PAPER
    * Every token follows its Regular Expression (paper section IX) and its
      Transition Diagram (paper section X).
    * A token is only accepted when the character right after it is one of
      the token's allowed DELIMITERS (paper section VIII, the delim_... sets).
      In the transition diagrams this is the last arrow into the final state.
    * If the diagram gets "stuck" (no arrow for the next character), the
      characters read so far are reported as ONE invalid lexeme, and reading
      starts again from the character where it got stuck.

WHO USES THIS FILE
    * app.py (the web app) creates a Lexer, calls tokenize(), and sends the
      tokens and errors to the browser.
    * You can also run it from a terminal:  python LimeLexer.py program.txt
"""
import sys


# ==========================================================================
#  LIMITS FROM THE PAPER
#  Numbers that the rules put a hard limit on.  Changing a value here changes
#  the lexer everywhere.
# ==========================================================================
MAX_IDENTIFIER_LENGTH = 30          # Identifiers rule 3: at most 30 characters
MAX_INT_DIGITS = 20                 # int_lit: a nonzero digit + up to 19 more
MAX_FRAC_DIGITS = 20                # flo_lit: up to 20 digits after the '.'
ESCAPE_CHARS = ('n', 't', '\\', '"')  # escapeseq: \n  \t  \\  \"
STRING_ALLOWS_RAW_TAB = True        # utf8_str includes tab (U+0009)
STRING_ALLOWS_RAW_NEWLINE = True    # utf8_str includes newline (U+000A)


# ==========================================================================
#  TOKEN AND ERROR RECORDS
#  Two small "containers": one describes a token that was found, the other
#  describes a lexical error.  app.py turns them into the rows of the Token
#  Output table and the cards of the Error / Console Log.
# ==========================================================================
class Token:
    """One token found in the source code."""

    def __init__(self, ttype, lexeme, line, col, category, pattern, flagged=False):
        self.type = ttype            # token name from the paper: Vary, +=, id, int_lit ...
        self.lexeme = lexeme         # the exact text from the source code
        self.line = line             # line number (starts at 1)
        self.col = col               # column number (starts at 1)
        self.category = category     # declaration / datatype / operator / literal ...
        self.pattern = pattern       # the token's regular expression from the paper
        self.flagged = flagged       # True = invalid (bad delimiter). Flagged tokens
                                     # are removed from the output and shown as errors.

    def __repr__(self):
        return "Token(%s, %r, %d:%d)" % (self.type, self.lexeme, self.line, self.col)


class LexicalError(Exception):
    """One lexical error: where it is, what was found, and why it is wrong."""

    def __init__(self, line, col, message, found="", expected="",
                 lexeme="", length=1, kind="Lexical error"):
        Exception.__init__(self, "%d:%d %s" % (line, col, message))
        self.line = line
        self.col = col
        self.message = message       # the reason it failed
        self.found = found           # the character / text that caused it
        self.expected = expected     # what the paper allows there instead
        self.lexeme = lexeme         # the invalid lexeme (shown as "Invalid lexeme:")
        self.length = length         # how many characters are wrong
        self.kind = kind             # short label, e.g. "Invalid delimiter"
        self.errors = [self]


# ==========================================================================
#  CHARACTER SETS  (paper section VIII, first part of Regular Definitions)
#  Each small function answers "does this character belong to this set?",
#  e.g. is_letter(c) is the set "letters".  End of file is represented by ''
#  (an empty string) and counts as a newline for delimiter checks.
# ==========================================================================
def is_lower(c):                            # lowercase: a-z and ñ
    if c == '':
        return False
    if 'a' <= c <= 'z':
        return True
    if c == 'ñ':                       # ñ
        return True
    return False


def is_upper(c):                            # uppercase: A-Z and Ñ
    if c == '':
        return False
    if 'A' <= c <= 'Z':
        return True
    if c == 'Ñ':                       # Ñ
        return True
    return False


def is_letter(c):                           # letters: lowercase, uppercase
    if is_lower(c):
        return True
    if is_upper(c):
        return True
    return False


def is_digit(c):                            # numbers: 0-9
    if c == '':
        return False
    if '0' <= c <= '9':
        return True
    return False


def is_nonzero_digit(c):                    # nonzero: 1-9
    if c == '':
        return False
    if '1' <= c <= '9':
        return True
    return False


def is_lets_nums(c):                        # lets_nums: letters, numbers
    if is_letter(c):
        return True
    if is_digit(c):
        return True
    return False


def is_id_char(c):                          # characters allowed inside an identifier: lets_nums / _
    if is_lets_nums(c):
        return True
    if c == '_':
        return True
    return False


def is_whitespace(c):                       # whitespace: space, tab
    if c == ' ':
        return True
    if c == '\t':
        return True
    return False


def is_newline(c):                          # newline (end of file also counts as one)
    if c == '\n':
        return True
    if c == '':
        return True
    return False


def is_control_char(c):                     # control characters: U+0000-U+001F and U+007F
    if c == '':
        return False
    code = ord(c)
    if code < 32:
        return True
    if code == 127:
        return True
    return False


def is_utf8_comm(c):
    """utf8_comm: any character except control characters (tab IS allowed)."""
    if c == '':
        return False
    if c == '\t':
        return True
    return not is_control_char(c)


def is_utf8_no_oppa(c):
    """utf8_no_oppa: like utf8_comm but without '(' - the first character
    after '#' in a single-line comment (a '(' would start a multi-line one)."""
    return is_utf8_comm(c) and c != '('


# ==========================================================================
#  DELIMITER SETS  (paper section VIII, the delim_... rows)
#  Each function answers: "may this character come RIGHT AFTER the token?"
#  This is the last arrow before the final state (*) in every transition
#  diagram.  The name in the comment is the exact name used in the paper.
# ==========================================================================
def d_oppa(c):                              # TD label "(" : built-in functions (Absorb, Squeeze ...)
    return c == '('


def d_squa_only(c):                         # TD label "[" : Basket
    return c == '['


def d_space(c):                             # TD label "space" : Vary, Same, Blend, Recipe
    return c == ' '


def d_arco(c):                              # delim_arco: space (arithmetic, assignment, comparison operators)
    return c == ' '


def d_ctrl(c):                              # delim_ctrl: space, (
    if c == ' ' or c == '(':
        return True
    return False


def d_blan(c):                              # delim_blan: newline, space, {, #
    if is_newline(c):
        return True
    if c == ' ' or c == '{' or c == '#':
        return True
    return False


def d_taun(c):                              # delim_taun: newline, space, {, #
    if is_newline(c):
        return True
    if c == ' ' or c == '{' or c == '#':
        return True
    return False


def d_type(c):                              # delim_type: newline, space, comma, ), {, [, #
    if is_newline(c):
        return True
    if c == ' ' or c == ',' or c == ')':
        return True
    if c == '{' or c == '[' or c == '#':
        return True
    return False


def d_reup(c):                              # delim_reup: newline, whitespace, semi_colon, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '}' or c == '#':
        return True
    return False


def d_prod(c):                              # delim_prod: newline, space, semi_colon, (, }, #
    if is_newline(c):
        return True
    if c == ' ' or c == ';' or c == '(' or c == '}' or c == '#':
        return True
    return False


def d_bool(c):                              # delim_bool: newline, whitespace, comma, semi_colon, ), ], {, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_unar(c):                              # delim_unar: newline, whitespace, comma, semi_colon, ), ], }, #
    # No letters: '++' and '--' must be separated from their identifier by a
    # space, so '++a' / '--a' are lexical errors.
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';' or c == ')' or c == ']':
        return True
    if c == '}' or c == '#':
        return True
    return False


def d_neg(c):                               # delim_neg: letters, (
    # Unary negation: '-a', '-ToNumber(w)', '-(x + 1)'.  A digit never gets
    # here because '-5' is read as ONE negative number token.
    if is_letter(c):
        return True
    return c == '('


def d_letters(c):                           # TD label "letters": after '.' (struct member, e.g. p.x)
    return is_letter(c)


def d_coma(c):                              # delim_coma: lets_nums, space, -, ", (, [
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '-' or c == '"' or c == '(' or c == '[':
        return True
    return False


def d_pare(c):                              # delim_pare: lets_nums, space, semi_colon, -, ", (, )
    if is_lets_nums(c):
        return True
    if c == ' ' or c == ';' or c == '-' or c == '"' or c == '(' or c == ')':
        return True
    return False


def d_clpa(c):                              # delim_clpa: newline, whitespace, comma, semi_colon, ), ], {, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';' or c == ')' or c == ']':
        return True
    if c == '{' or c == '}' or c == '#':
        return True
    return False


def d_clsq(c):                              # delim_clsq: same as delim_clpa plus [
    if c == '[':
        return True
    return d_clpa(c)


def d_squa(c):                              # delim_squa: lets_nums, space, -, (, [, ], "
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '-' or c == '(' or c == '[' or c == ']' or c == '"':
        return True
    return False


def d_brac(c):                              # delim_brac: letters, newline, whitespace, +, -, }, #
    if is_letter(c) or is_newline(c) or is_whitespace(c):
        return True
    if c == '+' or c == '-' or c == '}' or c == '#':
        return True
    return False


def d_clbr(c):                              # delim_clbr: newline, whitespace, semi_colon, #, }
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '#' or c == '}':
        return True
    return False


def d_colo(c):                              # delim_colo: N, R, W, T, space
    if c == 'N' or c == 'R' or c == 'W' or c == 'T' or c == ' ':
        return True
    return False


def d_arrw(c):                              # delim_arrw: B, N, R, W, T, space
    if c == 'B':
        return True
    return d_colo(c)


def d_semi(c):                              # delim_semi: lets_nums, newline, whitespace, semi_colon, +, -, (, ), }, #, "
    if is_lets_nums(c) or is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '+' or c == '-' or c == '(' or c == ')':
        return True
    if c == '}' or c == '#' or c == '"':
        return True
    return False


def d_newline(c):                           # TD label "newline": ends a single-line comment
    return is_newline(c)


def d_muco(c):                              # delim_muco: newline, whitespace (after ')#')
    if is_newline(c) or is_whitespace(c):
        return True
    return False


def d_id(c):                                # delim_id: newline, whitespace, comma, semi_colon, period, ), ], {, }, #, (, [, :
    # No operators: every binary operator needs a space before it, so
    # 'x>5' or 'x=5' is an error.
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';' or c == '.':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    if c == '(' or c == '[' or c == ':':
        return True
    return False


def d_str(c):                               # delim_str: newline, whitespace, comma, semi_colon, ), ], {, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_int(c):                               # delim_int: newline, whitespace, comma, semi_colon, ), ], {, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ',' or c == ';':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_flo(c):                               # delim_flo: same members as delim_int
    return d_int(c)


# Lookup table: delimiter name -> (the check function, the text shown in the
# "Expected:" line of an error).  The names match the paper's delim_... names
# (without the "delim_" prefix); "(", "[", "space", "letters" and "newline"
# are the labels the transition diagrams write directly on the arrow.
DELIMS = {
    '(':       (d_oppa, "'('"),
    '[':       (d_squa_only, "'['"),
    'space':   (d_space, "a space"),
    'arco':    (d_arco, "a space"),
    'ctrl':    (d_ctrl, "a space or '('"),
    'blan':    (d_blan, "a newline, space, '{' or '#'"),
    'taun':    (d_taun, "a newline, space, '{' or '#'"),
    'type':    (d_type, "a newline, space, ',', ')', '{', '[' or '#'"),
    'reup':    (d_reup, "a newline, space/tab, ';', '}' or '#'"),
    'prod':    (d_prod, "a newline, space, ';', '(', '}' or '#'"),
    'bool':    (d_bool, "a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
    'unar':    (d_unar, "a newline, space/tab, ',', ';', ')', ']', '}' or '#'"),
    'neg':     (d_neg, "a letter or '('"),
    'letters': (d_letters, "a letter"),
    'coma':    (d_coma, "a letter, digit, space, '-', '\"', '(' or '['"),
    'pare':    (d_pare, "a letter, digit, space, ';', '-', '\"', '(' or ')'"),
    'clpa':    (d_clpa, "a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
    'clsq':    (d_clsq, "'[', or a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
    'squa':    (d_squa, "a letter, digit, space, '-', '(', '[', ']' or '\"'"),
    'brac':    (d_brac, "a letter, newline, space/tab, '+', '-', '}' or '#'"),
    'clbr':    (d_clbr, "a newline, space/tab, ';', '#' or '}'"),
    'colo':    (d_colo, "a space, or one of 'N', 'R', 'W', 'T'"),
    'arrw':    (d_arrw, "a space, or one of 'B', 'N', 'R', 'W', 'T'"),
    'semi':    (d_semi, "a letter, digit, newline, space/tab, ';', '+', '-', '(', ')', '}', '#' or '\"'"),
    'newline': (d_newline, "a newline"),
    'muco':    (d_muco, "a newline or space/tab"),
    'id':      (d_id, "a newline, space/tab, ',', ';', '.', ')', ']', '{', '}', '#', '(', '[' or ':'"),
    'str':     (d_str, "a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
    'int':     (d_int, "a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
    'flo':     (d_flo, "a newline, space/tab, ',', ';', ')', ']', '{', '}' or '#'"),
}


# ==========================================================================
#  SMALL HELPERS
# ==========================================================================
def show_char(c):
    """Turns a character into readable text for error messages
    (e.g. '\\n' becomes "newline", '' becomes "end of file")."""
    if c == '':
        return "end of file"
    if c == '\n':
        return "newline"
    if c == '\t':
        return "tab"
    if c == ' ':
        return "space"
    if is_control_char(c):
        return "control character U+%04X" % ord(c)
    return "'%s'" % c


def concat_pattern(text):
    """Builds the regular expression of a reserved word / symbol the way the
    paper writes it, e.g. Vary -> (V)(a)(r)(y)."""
    out = ""
    i = 0
    while i < len(text):
        out = out + "(" + text[i] + ")"
        i += 1
    return out


# The regular expressions from paper section IX, attached to each token.
PATTERN_ID = "(letters)(lets_nums/_/λ)29"
PATTERN_INT = "(zero)/(-/λ)(nonzero)(numbers/λ)¹⁹"
PATTERN_FLO = ("((-/λ)((zero)/(nonzero)(numbers/λ)¹⁹))(period)"
               "(numbers)(numbers/λ)¹⁹")
PATTERN_STR = '(")(utf8_str/escapeseq)*(")'
PATTERN_SINGLE = "(#)(utf8_no_oppa)(utf8_comm)*"
PATTERN_MULTI = "(#)(()((utf8_no_clpa/newline)/())+(utf8_no_clha/newline))*())+(#)"
PATTERN_EOF = "EOF"


# ==========================================================================
#  THE LEXER
# ==========================================================================
class Lexer:
    """Holds the source code and walks through it, producing tokens/errors."""

    # ---------------------------------------------------------------------
    # SETUP: store the source code and remember where every line starts, so
    # that any position can later be turned into "line:column".
    # ---------------------------------------------------------------------
    def __init__(self, source):
        source = source.replace("\r\n", "\n")    # Windows line endings -> \n
        source = source.replace("\r", "\n")      # old Mac line endings -> \n
        self.src = source
        self.n = len(source)
        self.pos = 0                 # where we are currently reading
        self.tokens = []             # valid tokens found so far
        self.invalid_tokens = []     # tokens removed because they were invalid
        self.errors = []             # lexical errors found so far
        self.line_starts = [0]       # position where each line begins
        i = 0
        while i < self.n:
            if source[i] == '\n':
                self.line_starts.append(i + 1)
            i += 1

    # ---------------------------------------------------------------------
    # READ ONE CHARACTER at position p.  Past the end of the file it returns
    # '' (end of file), so the scanners never crash at the end.
    # ---------------------------------------------------------------------
    def at(self, p):
        if p < 0:
            return ''
        if p < self.n:
            return self.src[p]
        return ''

    # ---------------------------------------------------------------------
    # POSITION -> LINE:COLUMN.  Finds which line a position is on (binary
    # search through line_starts) and how far into that line it is.
    # ---------------------------------------------------------------------
    def loc(self, p):
        lo = 0
        hi = len(self.line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.line_starts[mid] <= p:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, p - self.line_starts[lo] + 1

    # ---------------------------------------------------------------------
    # SAVE A TOKEN: records the text from start to end as a token.
    # ---------------------------------------------------------------------
    def emit(self, ttype, start, end, category, pattern, flagged=False):
        line, col = self.loc(start)
        self.tokens.append(Token(ttype, self.src[start:end], line, col,
                                 category, pattern, flagged))

    # ---------------------------------------------------------------------
    # SAVE AN ERROR at position p.
    # ---------------------------------------------------------------------
    def error(self, p, message, found="", expected="", lexeme="",
              length=1, kind="Lexical error"):
        line, col = self.loc(p)
        self.errors.append(LexicalError(line, col, message, found, expected,
                                        lexeme, length, kind))

    # ---------------------------------------------------------------------
    # DELIMITER CHECK: is character c allowed right after a token whose
    # delimiter set is `key`?  (Looks the set up in the DELIMS table.)
    # ---------------------------------------------------------------------
    def follow_ok(self, key, c):
        func = DELIMS[key][0]
        return func(c)

    # ---------------------------------------------------------------------
    # DELIMITER ERROR: the token itself was spelled correctly but the
    # character after it is not in its delimiter set, so the transition
    # diagram never reaches the final state.  Reports which character was
    # found and which ones were allowed.
    # ---------------------------------------------------------------------
    def follow_error(self, what, lexeme, key, start, follow_pos):
        c = self.at(follow_pos)
        sline, scol = self.loc(start)
        msg = ("Invalid follow character %s after %s '%s' (starting at %d:%d)."
               % (show_char(c), what, lexeme, sline, scol))
        self.error(follow_pos, msg, found=show_char(c),
                   expected=DELIMS[key][1], lexeme=lexeme,
                   kind="Invalid delimiter")

    # ---------------------------------------------------------------------
    # MAIN LOOP (state 0 of every transition diagram).
    # Looks at the current character and decides which kind of token starts
    # here, then hands the work to the matching scanner below.  Repeats
    # until the end of the file, then adds the EOF token.
    # ---------------------------------------------------------------------
    def tokenize(self, raise_on_error=False):
        while True:
            c = self.at(self.pos)

            if c == '':                                   # end of file -> stop
                break

            if c == ' ' or c == '\t':                     # spaces/tabs between tokens are skipped
                self.pos += 1
                continue

            if c == '\n':                                 # newline is its own token
                self.emit("newline", self.pos, self.pos + 1, "newline", "newline")
                self.pos += 1
                continue

            if c == '#':                                  # '#' starts a comment
                self.scan_comment()
                continue

            if c == '"':                                  # '"' starts a Word literal
                self.scan_string()
                continue

            if is_digit(c):                               # a digit starts a number
                self.scan_number()
                continue

            if c == '-' and is_digit(self.at(self.pos + 1)):
                # '-' directly followed by a digit is a NEGATIVE NUMBER
                # (one token, e.g. -5 or -0.5), not the minus operator.
                self.scan_number()
                continue

            if is_letter(c):                              # a letter starts a reserved word or an identifier
                self.scan_word()
                continue

            if c == '_':
                # '_' cannot start any token.  Report ONLY the underscore and
                # start again right after it ('_name' -> error on '_', then id 'name').
                self.error(self.pos,
                           "An identifier cannot start with an underscore; "
                           "the first character must be a letter "
                           "(Identifiers rule 2). The '_' was skipped and "
                           "tokenization starts again after it.",
                           found="'_'", expected="a letter",
                           lexeme="_", length=1,
                           kind="Invalid identifier")
                self.pos += 1
                continue

            self.scan_symbol(c)                           # everything else: operators and symbols

        # EOF marks the end of the file and acts as the delimiter of the last
        # token.  It is always the last token.
        self.emit("EOF", self.n, self.n, "eof", PATTERN_EOF)

        # Only VALID tokens are output.  Invalid (flagged) ones already have
        # an error, so they are moved out of the token list.
        self.invalid_tokens = [t for t in self.tokens if t.flagged]
        self.tokens = [t for t in self.tokens if not t.flagged]

        if raise_on_error and len(self.errors) > 0:
            first = self.errors[0]
            first.errors = self.errors
            raise first
        return self.tokens

    # ---------------------------------------------------------------------
    # RESERVED WORDS  (Transition diagram X.A)
    # Follows the reserved-word diagram letter by letter: each nested `if`
    # is one arrow in the diagram.  If the letters spell a reserved word it
    # returns (lexeme, token name, delimiter set, category, length);
    # otherwise None.  The delimiter set is the label on the last arrow of
    # that word in the diagram.
    # ---------------------------------------------------------------------
    def match_reserved(self, p):
        if self.at(p + 0) == 'A':
            if self.at(p + 1) == 'b':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 'b':
                                return ('Absorb', 'Absorb', '(', 'builtin', 6)
            elif self.at(p + 1) == 'n':
                if self.at(p + 2) == 'd':
                    return ('And', 'And', 'ctrl', 'logical', 3)
            elif self.at(p + 1) == 'p':
                if self.at(p + 2) == 'p':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'n':
                            if self.at(p + 5) == 'd':
                                return ('Append', 'Append', '(', 'builtin', 6)
        elif self.at(p + 0) == 'B':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'k':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 't':
                                return ('Basket', 'Basket', '[', 'declaration', 6)
            elif self.at(p + 1) == 'l':
                if self.at(p + 2) == 'a':
                    if self.at(p + 3) == 'n':
                        if self.at(p + 4) == 'd':
                            return ('Bland', 'Bland', 'blan', 'datatype', 5)
                elif self.at(p + 2) == 'e':
                    if self.at(p + 3) == 'n':
                        if self.at(p + 4) == 'd':
                            return ('Blend', 'Blend', 'space', 'declaration', 5)
        elif self.at(p + 0) == 'C':
            if self.at(p + 1) == 'l':
                if self.at(p + 2) == 'e':
                    if self.at(p + 3) == 'a':
                        if self.at(p + 4) == 'r':
                            return ('Clear', 'Clear', '(', 'builtin', 5)
        elif self.at(p + 0) == 'F':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'c':
                    if self.at(p + 3) == 't':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 'r':
                                return ('Factor', 'Factor', 'ctrl', 'control', 6)
                elif self.at(p + 2) == 'l':
                    if self.at(p + 3) == 's':
                        if self.at(p + 4) == 'e':
                            return ('False', 'boo_lit', 'bool', 'literal', 5)
        elif self.at(p + 0) == 'H':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'v':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 's':
                                if self.at(p + 6) == 't':
                                    return ('Harvest', 'Harvest', 'ctrl', 'control', 7)
        elif self.at(p + 0) == 'I':
            if self.at(p + 1) == 'n':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 't':
                                return ('Insert', 'Insert', '(', 'builtin', 6)
        elif self.at(p + 0) == 'L':
            if self.at(p + 1) == 'e':
                if self.at(p + 2) == 'n':
                    if self.at(p + 3) == 'g':
                        if self.at(p + 4) == 't':
                            if self.at(p + 5) == 'h':
                                return ('Length', 'Length', '(', 'builtin', 6)
        elif self.at(p + 0) == 'M':
            if self.at(p + 1) == 'i':
                if self.at(p + 2) == 'x':
                    return ('Mix', 'Mix', 'ctrl', 'control', 3)
        elif self.at(p + 0) == 'N':
            if self.at(p + 1) == 'o':
                if self.at(p + 2) == 't':
                    return ('Not', 'Not', 'ctrl', 'logical', 3)
            elif self.at(p + 1) == 'u':
                if self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'b':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 'r':
                                return ('Number', 'Number', 'type', 'datatype', 6)
        elif self.at(p + 0) == 'O':
            if self.at(p + 1) == 'r':
                return ('Or', 'Or', 'ctrl', 'logical', 2)
        elif self.at(p + 0) == 'P':
            if self.at(p + 1) == 'r':
                if self.at(p + 2) == 'o':
                    if self.at(p + 3) == 'd':
                        if self.at(p + 4) == 'u':
                            if self.at(p + 5) == 'c':
                                if self.at(p + 6) == 'e':
                                    return ('Produce', 'Produce', 'prod', 'control', 7)
        elif self.at(p + 0) == 'R':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 't':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 'n':
                                if self.at(p + 6) == 'a':
                                    if self.at(p + 7) == 'l':
                                        return ('Rational', 'Rational', 'type', 'datatype', 8)
            elif self.at(p + 1) == 'e':
                if self.at(p + 2) == 'a':
                    if self.at(p + 3) == 'p':
                        return ('Reap', 'Reap', 'reup', 'control', 4)
                elif self.at(p + 2) == 'c':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'p':
                            if self.at(p + 5) == 'e':
                                return ('Recipe', 'Recipe', 'space', 'declaration', 6)
                elif self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'v':
                            if self.at(p + 5) == 'e':
                                return ('Remove', 'Remove', '(', 'builtin', 6)
        elif self.at(p + 0) == 'S':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'e':
                        return ('Same', 'Same', 'space', 'declaration', 4)
            elif self.at(p + 1) == 'q':
                if self.at(p + 2) == 'u':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 'z':
                                if self.at(p + 6) == 'e':
                                    return ('Squeeze', 'Squeeze', '(', 'builtin', 7)
            elif self.at(p + 1) == 't':
                if self.at(p + 2) == 'i':
                    if self.at(p + 3) == 'r':
                        return ('Stir', 'Stir', 'ctrl', 'control', 4)
        elif self.at(p + 0) == 'T':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 't':
                        if self.at(p + 4) == 'e':
                            return ('Taste', 'Taste', 'taun', 'control', 5)
            elif self.at(p + 1) == 'e':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 't':
                        return ('Test', 'Test', 'ctrl', 'control', 4)
            elif self.at(p + 1) == 'o':
                if self.at(p + 2) == 'N':
                    if self.at(p + 3) == 'u':
                        if self.at(p + 4) == 'm':
                            if self.at(p + 5) == 'b':
                                if self.at(p + 6) == 'e':
                                    if self.at(p + 7) == 'r':
                                        return ('ToNumber', 'ToNumber', '(', 'builtin', 8)
                elif self.at(p + 2) == 'R':
                    if self.at(p + 3) == 'a':
                        if self.at(p + 4) == 't':
                            if self.at(p + 5) == 'i':
                                if self.at(p + 6) == 'o':
                                    if self.at(p + 7) == 'n':
                                        if self.at(p + 8) == 'a':
                                            if self.at(p + 9) == 'l':
                                                return ('ToRational', 'ToRational', '(', 'builtin', 10)
                elif self.at(p + 2) == 'T':
                    if self.at(p + 3) == 'r':
                        if self.at(p + 4) == 'u':
                            if self.at(p + 5) == 't':
                                if self.at(p + 6) == 'h':
                                    return ('ToTruth', 'ToTruth', '(', 'builtin', 7)
                elif self.at(p + 2) == 'W':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 'd':
                                return ('ToWord', 'ToWord', '(', 'builtin', 6)
            elif self.at(p + 1) == 'r':
                if self.at(p + 2) == 'u':
                    if self.at(p + 3) == 'e':
                        return ('True', 'boo_lit', 'bool', 'literal', 4)
                    elif self.at(p + 3) == 't':
                        if self.at(p + 4) == 'h':
                            return ('Truth', 'Truth', 'type', 'datatype', 5)
                elif self.at(p + 2) == 'y':
                    return ('Try', 'Try', 'ctrl', 'control', 3)
        elif self.at(p + 0) == 'U':
            if self.at(p + 1) == 'n':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'p':
                            if self.at(p + 5) == 'e':
                                return ('Unripe', 'Unripe', 'taun', 'control', 6)
            elif self.at(p + 1) == 'p':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 't':
                                return ('Uproot', 'Uproot', 'reup', 'control', 6)
        elif self.at(p + 0) == 'V':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'y':
                        return ('Vary', 'Vary', 'space', 'declaration', 4)
        elif self.at(p + 0) == 'W':
            if self.at(p + 1) == 'o':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'd':
                        return ('Word', 'Word', 'type', 'datatype', 4)
        return None

    # ---------------------------------------------------------------------
    # WORDS: decides between a reserved word and an identifier.
    #   1. Try the reserved-word diagram.
    #   2. If it matched but a letter/digit/_ follows (e.g. "Varying"), it is
    #      really a longer identifier, so scan it as an identifier instead.
    #   3. Otherwise check the reserved word's delimiter.
    #   4. If nothing matched, it is an identifier.
    # ---------------------------------------------------------------------
    def scan_word(self):
        start = self.pos
        hit = self.match_reserved(start)
        if hit is not None:
            lexeme, ttype, dkey, category, length = hit
            follow_pos = start + length
            follow = self.at(follow_pos)
            if is_id_char(follow):
                self.scan_identifier()
                return
            if self.follow_ok(dkey, follow):
                self.emit(ttype, start, follow_pos, category,
                          concat_pattern(lexeme))
            else:
                if ttype == 'boo_lit':
                    what = "boolean literal"
                else:
                    what = "reserved word"
                self.emit(ttype, start, follow_pos, category,
                          concat_pattern(lexeme), flagged=True)
                self.follow_error(what, lexeme, dkey, start, follow_pos)
            self.pos = follow_pos
            return
        self.scan_identifier()

    # ---------------------------------------------------------------------
    # IDENTIFIERS  (Transition diagram X.C, RE (letters)(lets_nums/_/λ)29)
    # Reads a letter followed by letters, digits and underscores.
    #   * Longer than 30 characters: the diagram gets stuck after the 30th
    #     character, so those 30 are reported as an invalid lexeme and
    #     reading starts again at the 31st.
    #   * Otherwise the next character must be in delim_id.
    # ---------------------------------------------------------------------
    def scan_identifier(self):
        start = self.pos
        p = start + 1
        while is_id_char(self.at(p)):
            p += 1
        length = p - start
        if length > MAX_IDENTIFIER_LENGTH:
            cut = start + MAX_IDENTIFIER_LENGTH
            self.error(start,
                       "Identifier exceeds the %d-character limit "
                       "(Identifiers rule 3): after the %dth character %s is "
                       "neither part of the identifier nor a valid delimiter, "
                       "so the final state is never reached; tokenization "
                       "starts again at %s."
                       % (MAX_IDENTIFIER_LENGTH, MAX_IDENTIFIER_LENGTH,
                          show_char(self.at(cut)), show_char(self.at(cut))),
                       found=show_char(self.at(cut)) + " after 30 characters",
                       expected="an identifier of at most %d characters" % MAX_IDENTIFIER_LENGTH,
                       lexeme=self.src[start:cut], length=MAX_IDENTIFIER_LENGTH,
                       kind="Invalid identifier")
            self.pos = cut
            return
        lexeme = self.src[start:p]
        follow = self.at(p)
        if d_id(follow):
            self.emit("id", start, p, "identifier", PATTERN_ID)
        else:
            self.emit("id", start, p, "identifier", PATTERN_ID, flagged=True)
            self.follow_error("identifier", lexeme, 'id', start, p)
        self.pos = p

    # ---------------------------------------------------------------------
    # NUMBERS  (int_lit and flo_lit, Transition diagram X.C)
    # Reads an optional '-', the whole-number part, and an optional '.' with
    # the fractional part, then checks the delimiter.  Each error case below
    # is a place where the diagram gets stuck: the characters read so far are
    # one invalid lexeme and reading starts again where it got stuck.
    #   * '-0' not followed by '.'   (state 422 only has a 'period' arrow)
    #   * '0' followed by a digit    (leading zero, e.g. 007)
    #   * more than 20 digits        (whole part or fractional part)
    #   * '.' not followed by a digit (e.g. 360.)
    #   * a letter/_ right after the number (e.g. 9lives)
    # ---------------------------------------------------------------------
    def scan_number(self):
        start = self.pos
        p = start
        negative = False
        if self.at(p) == '-':                         # optional '-' of a negative number
            negative = True
            p += 1
        digit_start = p

        # -- whole-number part --
        if self.at(p) == '0':
            p += 1
            if negative and self.at(p) != '.':
                # '-0' is not a number: after '-' and '0' the only arrow is '.'
                self.error(start,
                           "'-0' is not a valid literal: after '-' and '0' the "
                           "transition diagram only allows '.' (a negative "
                           "float such as -0.5); found %s, so the final state "
                           "is never reached; tokenization starts again at %s."
                           % (show_char(self.at(p)), show_char(self.at(p))),
                           found=show_char(self.at(p)) + " after '-0'",
                           expected="'.' followed by digits (e.g. -0.5)",
                           lexeme=self.src[start:p], length=p - start,
                           kind="Invalid number")
                self.pos = p
                return
            if is_digit(self.at(p)):
                # leading zero: after '0' only a delimiter or '.' may follow
                self.error(start,
                           "Leading zero: an integer must be '0' alone or start "
                           "with a nonzero digit (Literals rule 1); %s cannot "
                           "follow '0', so the final state is never reached; "
                           "tokenization starts again at %s."
                           % (show_char(self.at(p)), show_char(self.at(p))),
                           found=show_char(self.at(p)) + " after '0'",
                           expected="'0' alone, or a number starting with 1-9",
                           lexeme=self.src[start:p], length=p - start,
                           kind="Invalid number")
                self.pos = p
                return
        else:
            p += 1
            while is_digit(self.at(p)):
                p += 1
        int_end = p
        int_digits = int_end - digit_start
        if int_digits > MAX_INT_DIGITS:
            # too many digits: the 20 digits read are invalid, restart at the 21st
            cut = digit_start + MAX_INT_DIGITS
            self.error(start,
                       "Integer literal exceeds the %d-digit limit (Literals "
                       "rule 1): the %dst digit is neither part of the literal "
                       "nor a valid delimiter, so the final state is never "
                       "reached; tokenization starts again at that digit."
                       % (MAX_INT_DIGITS, MAX_INT_DIGITS + 1),
                       found=show_char(self.at(cut)) + " after 20 digits",
                       expected="an integer of at most %d digits" % MAX_INT_DIGITS,
                       lexeme=self.src[start:cut], length=cut - start,
                       kind="Invalid number")
            self.pos = cut
            return

        # -- optional fractional part --
        if self.at(p) == '.':
            p += 1
            if not is_digit(self.at(p)):
                # '.' must be followed by at least one digit (e.g. 360. is invalid)
                self.error(start,
                           "A float literal needs at least one digit after the "
                           "decimal point (Literals rule 2); found %s after '.', "
                           "so the final state is never reached; tokenization "
                           "starts again at %s." % (show_char(self.at(p)), show_char(self.at(p))),
                           found="%s after '.'" % show_char(self.at(p)),
                           expected="a digit (0-9) after '.'",
                           lexeme=self.src[start:p], length=p - start,
                           kind="Invalid number")
                self.pos = p
                return
            frac_start = p
            while is_digit(self.at(p)):
                p += 1
            frac_digits = p - frac_start
            if frac_digits > MAX_FRAC_DIGITS:
                # too many digits after '.': restart at the 21st one
                cut = frac_start + MAX_FRAC_DIGITS
                self.error(start,
                           "Fractional part exceeds the %d-digit limit "
                           "(Literals rule 2): the %dst fractional digit is "
                           "neither part of the literal nor a valid delimiter, "
                           "so the final state is never reached; tokenization "
                           "starts again at that digit." % (MAX_FRAC_DIGITS, MAX_FRAC_DIGITS + 1),
                           found=show_char(self.at(cut)) + " after 20 fractional digits",
                           expected="at most %d digits after '.'" % MAX_FRAC_DIGITS,
                           lexeme=self.src[start:cut], length=cut - start,
                           kind="Invalid number")
                self.pos = cut
                return
            is_float = True
        else:
            is_float = False

        # -- the character after the number --
        follow = self.at(p)
        if is_id_char(follow):
            # number glued to letters (e.g. 9lives): the number is invalid,
            # reading starts again at the letters
            ttype = "flo_lit" if is_float else "int_lit"
            self.emit(ttype, start, p, "literal", PATTERN_FLO if is_float else PATTERN_INT,
                      flagged=True)
            self.error(start,
                       "Invalid lexeme: an identifier cannot start with a digit, "
                       "and a number cannot be glued to letters or underscores "
                       "(Identifiers rule 2); %s is not a valid delimiter after "
                       "'%s', so it is not tokenized and tokenization starts "
                       "again at %s."
                       % (show_char(follow), self.src[start:p], show_char(follow)),
                       found=show_char(follow) + " right after the number",
                       expected=DELIMS['flo' if is_float else 'int'][1],
                       lexeme=self.src[start:p], length=p - start,
                       kind="Invalid identifier")
            self.pos = p
            return
        if is_float:
            ok = d_flo(follow)
            key = 'flo'
            ttype = "flo_lit"
            pattern = PATTERN_FLO
            what = "float literal"
        else:
            ok = d_int(follow)
            key = 'int'
            ttype = "int_lit"
            pattern = PATTERN_INT
            what = "integer literal"
        if ok:
            self.emit(ttype, start, p, "literal", pattern)
        else:
            self.emit(ttype, start, p, "literal", pattern, flagged=True)
            self.follow_error(what, self.src[start:p], key, start, p)
        self.pos = p

    # ---------------------------------------------------------------------
    # WORD LITERALS / STRINGS  (RE (")(utf8_str/escapeseq)*("))
    # Reads from the opening " to the closing ".  Inside, allows any
    # character except control characters (tab and newline are allowed),
    # and only the escape sequences \n \t \\ \".  Reports a missing closing
    # quote, a bad escape (e.g. \f) or a control character.  Then checks
    # delim_str after the closing quote.
    # ---------------------------------------------------------------------
    def scan_string(self):
        start = self.pos
        p = start + 1
        bad = False
        closed = False
        while True:
            c = self.at(p)
            if c == '':                                   # reached end of file: never closed
                self.error(start, "Unterminated string literal: the closing "
                           "double quote '\"' was never found.",
                           found="end of file", expected="a closing '\"'",
                           lexeme=self.src[start:p], length=1,
                           kind="Unterminated string")
                bad = True
                break
            if c == '"':                                  # closing quote
                p += 1
                closed = True
                break
            if c == '\n':
                if STRING_ALLOWS_RAW_NEWLINE:
                    p += 1
                    continue
                self.error(start, "Unterminated string literal: the line ended "
                           "before the closing double quote '\"'.",
                           found="newline", expected="a closing '\"'",
                           lexeme=self.src[start:p], length=1,
                           kind="Unterminated string")
                bad = True
                break
            if c == '\\':                                 # escape sequence
                nxt = self.at(p + 1)
                if nxt != '' and nxt in ESCAPE_CHARS:
                    p += 2
                else:
                    allowed = ", ".join("\\" + e for e in ESCAPE_CHARS)
                    self.error(p, "Invalid escape sequence '\\%s'. Only %s are "
                               "allowed in a Word literal (Literals rule 4)." %
                               (nxt if (nxt != '' and nxt != '\n') else '', allowed),
                               found="'\\%s'" % (nxt if nxt != '\n' else ''),
                               expected=allowed,
                               lexeme=self.src[start:p + 2], length=2,
                               kind="Invalid escape sequence")
                    bad = True
                    if nxt == '' or nxt == '\n':
                        p += 1
                    else:
                        p += 2
                continue
            if c == '\t' and STRING_ALLOWS_RAW_TAB:
                p += 1
                continue
            if is_control_char(c):
                self.error(p, "Control character %s is not allowed inside a "
                           "Word literal (Literals rule 3); use an escape "
                           "sequence instead." % show_char(c),
                           found=show_char(c),
                           expected="a printable character or \\n, \\t, \\\\, \\\"",
                           lexeme=self.src[start:p + 1], length=1,
                           kind="Control character")
                bad = True
                p += 1
                continue
            p += 1                                        # ordinary character

        if not closed or bad:
            self.pos = p
            return
        follow = self.at(p)
        if d_str(follow):
            self.emit("str_lit", start, p, "literal", PATTERN_STR)
        else:
            self.emit("str_lit", start, p, "literal", PATTERN_STR, flagged=True)
            self.follow_error("string literal", self.src[start:p], 'str', start, p)
        self.pos = p

    # ---------------------------------------------------------------------
    # COMMENTS  (Transition diagram X.C, states 415-421)
    #
    # Multi-line  #( ... )#      RE (#)(()((utf8_no_clpa/newline)/())+(utf8_no_clha/newline))*())+(#)
    #   415 -'('-> 416, loop on any comment character or newline except ')'.
    #   ')' -> 417.  At 417: another ')' stays in 417, '#' -> 418 (closed),
    #   anything else goes back to 416 (that ')' was just comment text).
    #   So the FIRST ')#' closes the comment, and comments do not nest.
    #   After ')#' the delimiter must be delim_muco (newline or whitespace).
    #
    # Single-line  #text         RE (#)(utf8_no_oppa)(utf8_comm)*
    #   415 -utf8_no_oppa-> 420, loop on utf8_comm, newline -> 421 (final).
    #   The character after '#' may be ANY comment character except '('
    #   (a space is no longer required: '#note' and '# note' are both valid).
    #   A '#' followed directly by a newline, the end of the file, or a
    #   control character (other than tab) is an error.
    # ---------------------------------------------------------------------
    def scan_comment(self):
        start = self.pos
        if self.at(start + 1) == '(':
            # ---------------- multi-line comment ----------------
            q = start + 2                                # 416: inside the comment
            bad = False
            while True:
                c = self.at(q)
                if c == '':
                    self.error(start, "Unterminated multi-line comment: the "
                               "closing delimiter ')#' was never found, so the "
                               "rest of the file is swallowed by the comment.",
                               found="end of file", expected="')#'",
                               lexeme="#(", length=2, kind="Unterminated comment")
                    self.pos = q
                    return
                if c == ')' and self.at(q + 1) == '#':    # 417 -'#'-> 418: closed
                    break
                if c == '\n' or c == '\t':                # newline / tab allowed inside
                    q += 1
                    continue
                if is_control_char(c):
                    self.error(q, "Control character %s is not allowed inside a "
                               "comment (only tab and newline are)." % show_char(c),
                               found=show_char(c),
                               expected="a printable character, tab or newline",
                               lexeme="#(", length=1, kind="Control character")
                    bad = True
                q += 1
            end = q + 2                                   # just after ')#'
            if bad:
                self.pos = end
                return
            follow = self.at(end)
            if d_muco(follow):
                self.emit("multi_comm", start, end, "comment", PATTERN_MULTI)
            else:
                self.emit("multi_comm", start, end, "comment", PATTERN_MULTI,
                          flagged=True)
                self.follow_error("multi-line comment", ")#", 'muco', start, end)
            self.pos = end
            return

        # ---------------- single-line comment ----------------
        nxt = self.at(start + 1)
        if not is_utf8_no_oppa(nxt):
            # 415 has no arrow for this character: '#' alone is an invalid
            # lexeme.  Reading starts again right after the '#'.
            self.error(start,
                       "A single-line comment needs at least one comment "
                       "character after '#' (Comments rule 1); found %s, so "
                       "the final state is never reached." % show_char(nxt),
                       found=show_char(nxt) + " after '#'",
                       expected="any character except '(' (e.g. '# note' or '#note'), "
                                "or '#(' for a multi-line comment",
                       lexeme="#", length=1, kind="Invalid comment")
            self.pos = start + 1
            return
        q = start + 2                                     # 420: comment body
        bad = False
        while True:
            c = self.at(q)
            if c == '' or c == '\n':                      # newline / end of file -> 421 (final)
                break
            if not is_utf8_comm(c):
                self.error(q, "Control character %s is not allowed inside a "
                           "comment (only tab is)." % show_char(c),
                           found=show_char(c),
                           expected="a printable character or tab",
                           lexeme="#", length=1, kind="Control character")
                bad = True
            q += 1
        if not bad:
            self.emit("single_comm", start, q, "comment", PATTERN_SINGLE)
        self.pos = q

    # ---------------------------------------------------------------------
    # SAVE A SYMBOL: accepts the symbol `lexeme` at the current position if
    # the character after it is in its delimiter set; otherwise saves it as
    # invalid and reports a delimiter error.
    # ---------------------------------------------------------------------
    def sym(self, lexeme, dkey):
        start = self.pos
        end = start + len(lexeme)
        follow = self.at(end)
        if dkey in ('arco', 'unar', 'neg', 'arrw'):
            category = "operator"
        else:
            category = "delimiter"
        if self.follow_ok(dkey, follow):
            self.emit(lexeme, start, end, category, concat_pattern(lexeme))
        else:
            self.emit(lexeme, start, end, category, concat_pattern(lexeme),
                      flagged=True)
            self.follow_error("symbol", lexeme, dkey, start, end)
        self.pos = end

    # ---------------------------------------------------------------------
    # RESERVED SYMBOLS  (Transition diagram X.B)
    # Picks the LONGEST symbol that matches (e.g. '+=' before '+', '->'
    # before '-') and gives it the delimiter set from its diagram.  For '-':
    #   '-='  '--'  '->'          two-character symbols
    #   '-' + letter or '('       unary negation (delim_neg)
    #   '-' + digit               never reaches here (negative number)
    #   '-' otherwise             binary minus (delim_arco)
    # Characters that are not LIME symbols (e.g. @, $, ') are errors.
    # ---------------------------------------------------------------------
    def scan_symbol(self, c):
        p = self.pos
        c1 = self.at(p + 1)

        if c == '+':
            if c1 == '=':
                self.sym('+=', 'arco')
            elif c1 == '+':
                self.sym('++', 'unar')
            else:
                self.sym('+', 'arco')
        elif c == '-':
            if c1 == '=':
                self.sym('-=', 'arco')
            elif c1 == '-':
                self.sym('--', 'unar')
            elif c1 == '>':
                self.sym('->', 'arrw')
            elif d_neg(c1):
                self.sym('-', 'neg')
            else:
                self.sym('-', 'arco')
        elif c == '*':
            if c1 == '=':
                self.sym('*=', 'arco')
            else:
                self.sym('*', 'arco')
        elif c == '/':
            if c1 == '=':
                self.sym('/=', 'arco')
            else:
                self.sym('/', 'arco')
        elif c == '%':
            if c1 == '=':
                self.sym('%=', 'arco')
            else:
                self.sym('%', 'arco')
        elif c == '^':
            self.sym('^', 'arco')
        elif c == '=':
            if c1 == '=':
                self.sym('==', 'arco')
            else:
                self.sym('=', 'arco')
        elif c == '>':
            if c1 == '=':
                self.sym('>=', 'arco')
            else:
                self.sym('>', 'arco')
        elif c == '<':
            if c1 == '=':
                self.sym('<=', 'arco')
            else:
                self.sym('<', 'arco')
        elif c == '!':
            if c1 == '=':
                self.sym('!=', 'arco')
            else:
                self.error(p, "A lone '!' is not a LIME symbol; it is only valid "
                           "as part of '!='. (Use 'Not' for logical negation.)",
                           found="'!' followed by %s" % show_char(c1),
                           expected="'=' to form '!='", lexeme="!", length=1,
                           kind="Illegal symbol")
                self.pos = p + 1
        elif c == '(':
            self.sym('(', 'pare')
        elif c == ')':
            self.sym(')', 'clpa')
        elif c == '[':
            self.sym('[', 'squa')
        elif c == ']':
            self.sym(']', 'clsq')
        elif c == '{':
            self.sym('{', 'brac')
        elif c == '}':
            self.sym('}', 'clbr')
        elif c == ':':
            self.sym(':', 'colo')
        elif c == ';':
            self.sym(';', 'semi')
        elif c == '.':
            self.sym('.', 'letters')
        elif c == ',':
            self.sym(',', 'coma')
        elif c == "'":
            self.error(p, "Single quotes are invalid; Word literals must use "
                       "double quotes (Literals rule 3).",
                       found="\"'\"", expected="a double quote '\"'",
                       lexeme="'", length=1, kind="Illegal character")
            self.pos = p + 1
        else:
            if is_control_char(c):
                msg = "Control character %s is not allowed here." % show_char(c)
            else:
                msg = ("Illegal character %s: it does not belong to the LIME "
                       "alphabet." % show_char(c))
            self.error(p, msg, found=show_char(c),
                       expected="a LIME token", lexeme=c, length=1,
                       kind="Illegal character")
            self.pos = p + 1


# ==========================================================================
#  SHORTCUT: tokenize(source) in one call (used for quick tests).
# ==========================================================================
def tokenize(source, raise_on_error=True):
    lx = Lexer(source)
    return lx.tokenize(raise_on_error=raise_on_error)


# ==========================================================================
#  TERMINAL MODE
#  `python LimeLexer.py program.txt` prints every token and every error.
#  With no file name it reads the code typed / piped into the terminal.
# ==========================================================================
def run_cli(path):
    if path == "-":
        source = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
    lexer = Lexer(source)
    lexer.tokenize()
    for tok in lexer.tokens:
        if tok.type == "newline":
            continue
        print("%4d:%-3d %-12s %r" % (tok.line, tok.col, tok.type, tok.lexeme))
    for err in lexer.errors:
        print("ERROR %d:%d [%s] %s | expected: %s"
              % (err.line, err.col, err.kind, err.message, err.expected))
    print("%d tokens, %d errors" % (
        len([t for t in lexer.tokens if t.type != "newline"]), len(lexer.errors)))
    return 1 if lexer.errors else 0


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "-"
    if path == "--cli":                     # old flag still accepted
        path = sys.argv[2] if len(sys.argv) > 2 else "-"
    sys.exit(run_cli(path))


if __name__ == "__main__":
    main()