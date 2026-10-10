import sys

# --------------------------------------------------------------------------
# Tunable spec constants
# --------------------------------------------------------------------------
MAX_IDENTIFIER_LENGTH = 30          # Identifiers rule 3
MAX_INT_DIGITS = 10                 # int_lit: nonzero digit + up to 9 more
MAX_FRAC_DIGITS = 10                # flo_lit: fractional part up to 10 digits
INT_MAX = 2147483647                # Number is a signed 32-bit integer
INT_MIN_MAGNITUDE = 2147483648      # magnitude of the smallest Number: -2147483648
ESCAPE_CHARS = ('n', 't', '\\', '"')
STRING_ALLOWS_RAW_TAB = True        
STRING_ALLOWS_RAW_NEWLINE = True  


# ==========================================================================
#  Data structures
# ==========================================================================
class Token:
    """One lexeme produced by the lexer."""

    def __init__(self, ttype, lexeme, line, col, category, pattern, flagged=False):
        self.type = ttype            # spec token name: Vary, +=, id, int_lit ...
        self.lexeme = lexeme         # exact source text
        self.line = line             # 1-based
        self.col = col               # 1-based
        self.category = category     # declaration / datatype / operator / ...
        self.pattern = pattern       # regular expression from the spec
        self.flagged = flagged       # True: lexeme valid but its follow char was not

    def __repr__(self):
        return "Token(%s, %r, %d:%d)" % (self.type, self.lexeme, self.line, self.col)


class LexicalError(Exception):
    """A lexical error with an exact location and an explanation."""

    def __init__(self, line, col, message, found="", expected="",
                 lexeme="", length=1, kind="Lexical error"):
        Exception.__init__(self, "%d:%d %s" % (line, col, message))
        self.line = line
        self.col = col
        self.message = message       # WHY it failed
        self.found = found           # the faulty character / sequence
        self.expected = expected     # what the spec allows here
        self.lexeme = lexeme         # the token being scanned (if any)
        self.length = length         # characters to highlight in the editor
        self.kind = kind
        self.errors = [self]


# ==========================================================================
#  Character classes
# ==========================================================================
def is_lower(c):
    if c == '':
        return False
    if 'a' <= c <= 'z':
        return True
    if c == '\u00f1':                       # n with tilde
        return True
    return False


def is_upper(c):
    if c == '':
        return False
    if 'A' <= c <= 'Z':
        return True
    if c == '\u00d1':                       # N with tilde
        return True
    return False


def is_letter(c):
    if is_lower(c):
        return True
    if is_upper(c):
        return True
    return False


def is_digit(c):
    if c == '':
        return False
    if '0' <= c <= '9':
        return True
    return False


def is_nonzero_digit(c):
    if c == '':
        return False
    if '1' <= c <= '9':
        return True
    return False


def is_lets_nums(c):
    if is_letter(c):
        return True
    if is_digit(c):
        return True
    return False


def is_id_char(c):                          # lets_nums / _
    if is_lets_nums(c):
        return True
    if c == '_':
        return True
    return False


def is_space(c):
    return c == ' '


def is_whitespace(c):                       # space, tab
    if c == ' ':
        return True
    if c == '\t':
        return True
    return False


def is_newline(c):                          # EOF acts as an implicit newline
    if c == '\n':
        return True
    if c == '':
        return True
    return False


def is_arith_op(c):
    if c == '+' or c == '-' or c == '*':
        return True
    if c == '/' or c == '%' or c == '^':
        return True
    return False


def is_compare_op(c):
    if c == '>' or c == '<':
        return True
    return False


def is_assign_op(c):
    return c == '='


def is_control_char(c):                     # U+0000-U+001F or U+007F
    if c == '':
        return False
    code = ord(c)
    if code < 32:
        return True
    if code == 127:
        return True
    return False


# ==========================================================================
#  Delimiter sets
# ==========================================================================
def d_func(c):                              # delim_func
    return c == '('


def d_bask(c):                              # delim_bask
    return c == '['


def d_spac(c):                              # delim_spac
    return c == ' '


def d_ctrl(c):                              # space, (
    if c == ' ' or c == '(':
        return True
    return False


def d_blan(c):                              # newline, space, {, #
    if is_newline(c):
        return True
    if c == ' ' or c == '{' or c == '#':
        return True
    return False


def d_taun(c):                              # same members as delim_blan
    if is_newline(c):
        return True
    if c == ' ' or c == '{' or c == '#':
        return True
    return False


def d_type(c):                              # newline, space, =, comma, ), {, [, #
    if is_newline(c):
        return True
    if c == ' ' or is_assign_op(c) or c == ',' or c == ')':
        return True
    if c == '{' or c == '[' or c == '#':
        return True
    return False


def d_reup(c):                              # newline, whitespace, ;, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '}' or c == '#':
        return True
    return False


def d_prod(c):                              # newline, space, ;, (, }, #
    if is_newline(c):
        return True
    if c == ' ' or c == ';' or c == '(' or c == '}' or c == '#':
        return True
    return False


def d_bool(c):                              # newline, whitespace, =, comma, ;, !, ), ], {, }, #
    if is_newline(c) or is_whitespace(c):
        return True
    if is_assign_op(c) or c == ',' or c == ';' or c == '!':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_arco(c):                              # lets_nums, space, -, (
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '-' or c == '(':
        return True
    return False


def d_minu(c):                              # lets_nums, space, (
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '(':
        return True
    return False


def d_aras(c):                              # ", delim_arco
    if c == '"':
        return True
    return d_arco(c)


def d_unar(c):                              # ++ / --
    if is_newline(c) or is_whitespace(c) or is_letter(c):
        return True
    if is_arith_op(c) or is_compare_op(c) or is_assign_op(c):
        return True
    if c == ',' or c == ';' or c == '!' or c == ')' or c == ']':
        return True
    if c == '}' or c == '#':
        return True
    return False


def d_strc(c):                              # '.'  ->  letters
    return is_letter(c)


def d_coma(c):                              # lets_nums, space, -, ", (, [
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '-' or c == '"' or c == '(' or c == '[':
        return True
    return False


def d_pare(c):                              # '('
    if is_lets_nums(c):
        return True
    if c == ' ' or c == ';' or c == '-' or c == '"' or c == '(' or c == ')':
        return True
    return False


def d_clpa(c):                              # ')'
    if is_newline(c) or is_whitespace(c):
        return True
    if is_arith_op(c) or is_compare_op(c) or is_assign_op(c):
        return True
    if c == ',' or c == ';' or c == '!' or c == ')' or c == ']':
        return True
    if c == '{' or c == '}' or c == '#':
        return True
    return False


def d_clsq(c):                              # ']'  ->  [ , delim_clpa
    if c == '[':
        return True
    return d_clpa(c)


def d_squa(c):                              # '['
    if is_lets_nums(c):
        return True
    if c == ' ' or c == '-' or c == '(' or c == '[' or c == ']' or c == '"':
        return True
    return False


def d_brac(c):                              # '{'
    if is_letter(c) or is_newline(c) or is_whitespace(c):
        return True
    if c == '+' or c == '-' or c == '}' or c == '#':
        return True
    return False


def d_clbr(c):                              # '}'
    if is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '#' or c == '}':
        return True
    return False


def d_colo(c):                              # ':'  ->  N, R, W, T, space
    if c == 'N' or c == 'R' or c == 'W' or c == 'T' or c == ' ':
        return True
    return False


def d_arrw(c):                              # '->'  ->  B, delim_colo
    if c == 'B':
        return True
    return d_colo(c)


def d_semi(c):                              # ';'
    if is_lets_nums(c) or is_newline(c) or is_whitespace(c):
        return True
    if c == ';' or c == '+' or c == '-' or c == '(' or c == ')':
        return True
    if c == '}' or c == '#' or c == '"':
        return True
    return False


def d_sico(c):                              # single-line comment ends at newline
    return is_newline(c)


def d_muco(c):                              # after ')#': newline, whitespace
    if is_newline(c) or is_whitespace(c):
        return True
    return False


def d_id(c):                                # identifiers
    if is_newline(c) or is_whitespace(c):
        return True
    if is_compare_op(c) or is_assign_op(c):     # arith_op removed: needs a space first
        return True
    if c == ',' or c == ';' or c == '.' or c == '!':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    if c == '(' or c == '[' or c == ':':
        return True
    return False


def d_str(c):                               # string literals
    if is_newline(c) or is_whitespace(c):
        return True
    if c == '+' or is_assign_op(c) or c == ',' or c == ';' or c == '!':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_int(c):                               # int_lit (and flo_lit)
    if is_newline(c) or is_whitespace(c):
        return True
    if is_compare_op(c) or is_assign_op(c):     # arith_op removed: needs a space first
        return True
    if c == ',' or c == ';' or c == '!':
        return True
    if c == ')' or c == ']' or c == '{' or c == '}' or c == '#':
        return True
    return False


def d_flo(c):                               # delim_flo = delim_int
    return d_int(c)


DELIMS = {
    'func': (d_func, "'('"),
    'bask': (d_bask, "'['"),
    'spac': (d_spac, "a space"),
    'ctrl': (d_ctrl, "a space or '('"),
    'blan': (d_blan, "a newline, space, '{' or '#'"),
    'taun': (d_taun, "a newline, space, '{' or '#'"),
    'type': (d_type, "a newline, space, '=', ',', ')', '{', '[' or '#'"),
    'reup': (d_reup, "a newline, space/tab, ';', '}' or '#'"),
    'prod': (d_prod, "a newline, space, ';', '(', '}' or '#'"),
    'bool': (d_bool, "a newline, space/tab, '=', ',', ';', '!', ')', ']', '{', '}' or '#'"),
    'arco': (d_arco, "a letter, digit, space, '-' or '('"),
    'minu': (d_minu, "a letter, digit, space or '('"),
    'aras': (d_aras, "a '\"', letter, digit, space, '-' or '('"),
    'unar': (d_unar, "a newline, space/tab, letter, operator, ',', ';', '!', ')', ']', '}' or '#'"),
    'strc': (d_strc, "a letter"),
    'coma': (d_coma, "a letter, digit, space, '-', '\"', '(' or '['"),
    'pare': (d_pare, "a letter, digit, space, ';', '-', '\"', '(' or ')'"),
    'clpa': (d_clpa, "a newline, space/tab, operator, ',', ';', '!', ')', ']', '{', '}' or '#'"),
    'clsq': (d_clsq, "'[', or a newline, space/tab, operator, ',', ';', '!', ')', ']', '{', '}' or '#'"),
    'squa': (d_squa, "a letter, digit, space, '-', '(', '[', ']' or '\"'"),
    'brac': (d_brac, "a letter, newline, space/tab, '+', '-', '}' or '#'"),
    'clbr': (d_clbr, "a newline, space/tab, ';', '#' or '}'"),
    'colo': (d_colo, "a space, or one of 'N', 'R', 'W', 'T'"),
    'arrw': (d_arrw, "a space, or one of 'B', 'N', 'R', 'W', 'T'"),
    'semi': (d_semi, "a letter, digit, newline, space/tab, ';', '+', '-', '(', ')', '}', '#' or '\"'"),
    'sico': (d_sico, "a newline"),
    'muco': (d_muco, "a newline or space/tab"),
    'id':   (d_id, "a newline, space/tab, '<', '>', '=', ',', ';', '.', '!', ')', ']', '{', '}', '#', '(', '[' or ':'"),
    'str':  (d_str, "a newline, space/tab, '+', '=', ',', ';', '!', ')', ']', '{', '}' or '#'"),
    'int':  (d_int, "a newline, space/tab, '<', '>', '=', ',', ';', '!', ')', ']', '{', '}' or '#'"),
    'flo':  (d_flo, "a newline, space/tab, '<', '>', '=', ',', ';', '!', ')', ']', '{', '}' or '#'"),
}


def show_char(c):
    """Printable description of a single character (or end of input)."""
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
    """Spec-style concatenation pattern, e.g. Vary -> (V)(a)(r)(y)."""
    out = ""
    i = 0
    while i < len(text):
        out = out + "(" + text[i] + ")"
        i += 1
    return out


PATTERN_ID = "(letters)(lets_nums/_/\u03bb)\u00b2\u2079"
PATTERN_INT = "(zero)/(-/\u03bb)(nonzero)(numbers/\u03bb)\u2079"
PATTERN_FLO = ("((zero)/(-/\u03bb)(nonzero)(numbers/\u03bb)\u2079)(period)"
               "(numbers)(numbers/\u03bb)\u2079")
PATTERN_STR = '(")(utf8_str/escapeseq)*(")'
PATTERN_SINGLE = "(#)(utf8_comm)*"
PATTERN_MULTI = "(#)(()(utf8_comm/newline)*())(#)"


# ==========================================================================
#  The Lexer
# ==========================================================================
class Lexer:
    def __init__(self, source):
        # normalise line endings (pre-processing only, not tokenizing)
        source = source.replace("\r\n", "\n")
        source = source.replace("\r", "\n")
        self.src = source
        self.n = len(source)
        self.pos = 0
        self.tokens = []
        self.errors = []
        self.overflow_end = -1      # where the last over-long identifier ended
        # absolute offset of the first char of every line, for line:col
        self.line_starts = [0]
        i = 0
        while i < self.n:
            if source[i] == '\n':
                self.line_starts.append(i + 1)
            i += 1

    # ---------------------------------------------------------- helpers --
    def at(self, p):
        """Character at absolute offset p, or '' past the end."""
        if p < 0:
            return ''
        if p < self.n:
            return self.src[p]
        return ''

    def loc(self, p):
        """(line, col), both 1-based, of absolute offset p (binary search)."""
        lo = 0
        hi = len(self.line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.line_starts[mid] <= p:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, p - self.line_starts[lo] + 1

    def emit(self, ttype, start, end, category, pattern, flagged=False):
        line, col = self.loc(start)
        self.tokens.append(Token(ttype, self.src[start:end], line, col,
                                 category, pattern, flagged))

    def error(self, p, message, found="", expected="", lexeme="",
              length=1, kind="Lexical error"):
        line, col = self.loc(p)
        self.errors.append(LexicalError(line, col, message, found, expected,
                                        lexeme, length, kind))

    def follow_ok(self, key, c):
        """Is c a legal follow character for delimiter set `key`?"""
        func = DELIMS[key][0]
        return func(c)

    def follow_error(self, what, lexeme, key, start, follow_pos):
        """Report an illegal follow character right after a matched lexeme."""
        c = self.at(follow_pos)
        if follow_pos == self.overflow_end and d_id(c):
            # This lexeme is the tail of an over-long identifier that was split at
            # the 30-character limit. The character after it is a legal follow
            # character for an identifier, so it is not a second error.
            if self.tokens:
                self.tokens[-1].flagged = False
            return
        sline, scol = self.loc(start)
        msg = ("Invalid follow character %s after %s '%s' (starting at %d:%d)."
               % (show_char(c), what, lexeme, sline, scol))
        self.error(follow_pos, msg, found=show_char(c),
                   expected=DELIMS[key][1], lexeme=lexeme,
                   kind="Invalid delimiter")

    # ------------------------------------------------------------- main --
    def tokenize(self, raise_on_error=False):
        """Scan the whole source. Returns the token list; errors are in
        self.errors. With raise_on_error=True a LexicalError (carrying all
        errors in `.errors`) is raised instead if anything went wrong."""
        while True:
            c = self.at(self.pos)

            if c == '':                                   # end of input
                break

            if c == ' ' or c == '\t':                     # skip blanks
                self.pos += 1
                continue

            if c == '\n':                                 # newline token
                self.emit("newline", self.pos, self.pos + 1, "newline", "newline")
                self.pos += 1
                continue

            if c == '#':                                  # comments
                self.scan_comment()
                continue

            if c == '"':                                  # string literal
                self.scan_string()
                continue

            if is_digit(c):                               # int / float literal
                self.scan_number()
                continue

            if c == '-' and is_nonzero_digit(self.at(self.pos + 1)):
                self.scan_number()                        # (-/lambda)(nonzero)...
                continue

            if is_letter(c):                              # reserved word / id
                self.scan_word()
                continue

            if c == '_':
                end = self.pos
                while is_id_char(self.at(end)):
                    end += 1
                self.error(self.pos,
                           "An identifier cannot start with an underscore; "
                           "the first character must be a letter "
                           "(Identifiers rule 2).",
                           found="'_'", expected="a letter",
                           lexeme=self.src[self.pos:end], length=end - self.pos,
                           kind="Invalid identifier")
                self.pos = end
                continue

            self.scan_symbol(c)                           # operators etc.

        if raise_on_error and len(self.errors) > 0:
            first = self.errors[0]
            first.errors = self.errors
            raise first
        return self.tokens

    # --------------------------------------------- reserved words (DFA) --
    def match_reserved(self, p):
        """Walk the reserved-word transition diagram one character at a time.

        Returns (lexeme, token_type, delimiter_key, category, length) when
        the letters from offset p spell a reserved word, otherwise None.
        Nothing is looked up in a table - every letter is its own `if`.
        """
        if self.at(p + 0) == 'A':
            if self.at(p + 1) == 'b':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 'b':
                                # reached the last letter of 'Absorb'
                                return ('Absorb', 'Absorb', 'func', 'builtin', 6)
            elif self.at(p + 1) == 'n':
                if self.at(p + 2) == 'd':
                    # reached the last letter of 'And'
                    return ('And', 'And', 'ctrl', 'logical', 3)
            elif self.at(p + 1) == 'p':
                if self.at(p + 2) == 'p':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'n':
                            if self.at(p + 5) == 'd':
                                # reached the last letter of 'Append'
                                return ('Append', 'Append', 'func', 'builtin', 6)
        elif self.at(p + 0) == 'B':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'k':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 't':
                                # reached the last letter of 'Basket'
                                return ('Basket', 'Basket', 'bask', 'declaration', 6)
            elif self.at(p + 1) == 'l':
                if self.at(p + 2) == 'a':
                    if self.at(p + 3) == 'n':
                        if self.at(p + 4) == 'd':
                            # reached the last letter of 'Bland'
                            return ('Bland', 'Bland', 'blan', 'datatype', 5)
                elif self.at(p + 2) == 'e':
                    if self.at(p + 3) == 'n':
                        if self.at(p + 4) == 'd':
                            # reached the last letter of 'Blend'
                            return ('Blend', 'Blend', 'spac', 'declaration', 5)
        elif self.at(p + 0) == 'C':
            if self.at(p + 1) == 'l':
                if self.at(p + 2) == 'e':
                    if self.at(p + 3) == 'a':
                        if self.at(p + 4) == 'r':
                            # reached the last letter of 'Clear'
                            return ('Clear', 'Clear', 'func', 'builtin', 5)
        elif self.at(p + 0) == 'F':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'c':
                    if self.at(p + 3) == 't':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 'r':
                                # reached the last letter of 'Factor'
                                return ('Factor', 'Factor', 'ctrl', 'control', 6)
                elif self.at(p + 2) == 'l':
                    if self.at(p + 3) == 's':
                        if self.at(p + 4) == 'e':
                            # reached the last letter of 'False'
                            return ('False', 'boo_lit', 'bool', 'literal', 5)
        elif self.at(p + 0) == 'H':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'v':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 's':
                                if self.at(p + 6) == 't':
                                    # reached the last letter of 'Harvest'
                                    return ('Harvest', 'Harvest', 'ctrl', 'control', 7)
        elif self.at(p + 0) == 'I':
            if self.at(p + 1) == 'n':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 't':
                                # reached the last letter of 'Insert'
                                return ('Insert', 'Insert', 'func', 'builtin', 6)
        elif self.at(p + 0) == 'L':
            if self.at(p + 1) == 'e':
                if self.at(p + 2) == 'n':
                    if self.at(p + 3) == 'g':
                        if self.at(p + 4) == 't':
                            if self.at(p + 5) == 'h':
                                # reached the last letter of 'Length'
                                return ('Length', 'Length', 'func', 'builtin', 6)
        elif self.at(p + 0) == 'M':
            if self.at(p + 1) == 'i':
                if self.at(p + 2) == 'x':
                    # reached the last letter of 'Mix'
                    return ('Mix', 'Mix', 'ctrl', 'control', 3)
        elif self.at(p + 0) == 'N':
            if self.at(p + 1) == 'o':
                if self.at(p + 2) == 't':
                    # reached the last letter of 'Not'
                    return ('Not', 'Not', 'ctrl', 'logical', 3)
            elif self.at(p + 1) == 'u':
                if self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'b':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 'r':
                                # reached the last letter of 'Number'
                                return ('Number', 'Number', 'type', 'datatype', 6)
        elif self.at(p + 0) == 'O':
            if self.at(p + 1) == 'r':
                # reached the last letter of 'Or'
                return ('Or', 'Or', 'ctrl', 'logical', 2)
        elif self.at(p + 0) == 'P':
            if self.at(p + 1) == 'r':
                if self.at(p + 2) == 'o':
                    if self.at(p + 3) == 'd':
                        if self.at(p + 4) == 'u':
                            if self.at(p + 5) == 'c':
                                if self.at(p + 6) == 'e':
                                    # reached the last letter of 'Produce'
                                    return ('Produce', 'Produce', 'prod', 'control', 7)
        elif self.at(p + 0) == 'R':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 't':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 'n':
                                if self.at(p + 6) == 'a':
                                    if self.at(p + 7) == 'l':
                                        # reached the last letter of 'Rational'
                                        return ('Rational', 'Rational', 'type', 'datatype', 8)
            elif self.at(p + 1) == 'e':
                if self.at(p + 2) == 'a':
                    if self.at(p + 3) == 'p':
                        # reached the last letter of 'Reap'
                        return ('Reap', 'Reap', 'reup', 'control', 4)
                elif self.at(p + 2) == 'c':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'p':
                            if self.at(p + 5) == 'e':
                                # reached the last letter of 'Recipe'
                                return ('Recipe', 'Recipe', 'spac', 'declaration', 6)
                elif self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'v':
                            if self.at(p + 5) == 'e':
                                # reached the last letter of 'Remove'
                                return ('Remove', 'Remove', 'func', 'builtin', 6)
        elif self.at(p + 0) == 'S':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'm':
                    if self.at(p + 3) == 'e':
                        # reached the last letter of 'Same'
                        return ('Same', 'Same', 'spac', 'declaration', 4)
            elif self.at(p + 1) == 'q':
                if self.at(p + 2) == 'u':
                    if self.at(p + 3) == 'e':
                        if self.at(p + 4) == 'e':
                            if self.at(p + 5) == 'z':
                                if self.at(p + 6) == 'e':
                                    # reached the last letter of 'Squeeze'
                                    return ('Squeeze', 'Squeeze', 'func', 'builtin', 7)
            elif self.at(p + 1) == 't':
                if self.at(p + 2) == 'i':
                    if self.at(p + 3) == 'r':
                        # reached the last letter of 'Stir'
                        return ('Stir', 'Stir', 'ctrl', 'control', 4)
        elif self.at(p + 0) == 'T':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 't':
                        if self.at(p + 4) == 'e':
                            # reached the last letter of 'Taste'
                            return ('Taste', 'Taste', 'taun', 'control', 5)
            elif self.at(p + 1) == 'e':
                if self.at(p + 2) == 's':
                    if self.at(p + 3) == 't':
                        # reached the last letter of 'Test'
                        return ('Test', 'Test', 'ctrl', 'control', 4)
            elif self.at(p + 1) == 'o':
                if self.at(p + 2) == 'N':
                    if self.at(p + 3) == 'u':
                        if self.at(p + 4) == 'm':
                            if self.at(p + 5) == 'b':
                                if self.at(p + 6) == 'e':
                                    if self.at(p + 7) == 'r':
                                        # reached the last letter of 'ToNumber'
                                        return ('ToNumber', 'ToNumber', 'func', 'builtin', 8)
                elif self.at(p + 2) == 'R':
                    if self.at(p + 3) == 'a':
                        if self.at(p + 4) == 't':
                            if self.at(p + 5) == 'i':
                                if self.at(p + 6) == 'o':
                                    if self.at(p + 7) == 'n':
                                        if self.at(p + 8) == 'a':
                                            if self.at(p + 9) == 'l':
                                                # reached the last letter of 'ToRational'
                                                return ('ToRational', 'ToRational', 'func', 'builtin', 10)
                elif self.at(p + 2) == 'T':
                    if self.at(p + 3) == 'r':
                        if self.at(p + 4) == 'u':
                            if self.at(p + 5) == 't':
                                if self.at(p + 6) == 'h':
                                    # reached the last letter of 'ToTruth'
                                    return ('ToTruth', 'ToTruth', 'func', 'builtin', 7)
                elif self.at(p + 2) == 'W':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'r':
                            if self.at(p + 5) == 'd':
                                # reached the last letter of 'ToWord'
                                return ('ToWord', 'ToWord', 'func', 'builtin', 6)
            elif self.at(p + 1) == 'r':
                if self.at(p + 2) == 'u':
                    if self.at(p + 3) == 'e':
                        # reached the last letter of 'True'
                        return ('True', 'boo_lit', 'bool', 'literal', 4)
                    elif self.at(p + 3) == 't':
                        if self.at(p + 4) == 'h':
                            # reached the last letter of 'Truth'
                            return ('Truth', 'Truth', 'type', 'datatype', 5)
                elif self.at(p + 2) == 'y':
                    # reached the last letter of 'Try'
                    return ('Try', 'Try', 'ctrl', 'control', 3)
        elif self.at(p + 0) == 'U':
            if self.at(p + 1) == 'n':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'i':
                        if self.at(p + 4) == 'p':
                            if self.at(p + 5) == 'e':
                                # reached the last letter of 'Unripe'
                                return ('Unripe', 'Unripe', 'taun', 'control', 6)
            elif self.at(p + 1) == 'p':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'o':
                        if self.at(p + 4) == 'o':
                            if self.at(p + 5) == 't':
                                # reached the last letter of 'Uproot'
                                return ('Uproot', 'Uproot', 'reup', 'control', 6)
        elif self.at(p + 0) == 'V':
            if self.at(p + 1) == 'a':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'y':
                        # reached the last letter of 'Vary'
                        return ('Vary', 'Vary', 'spac', 'declaration', 4)
        elif self.at(p + 0) == 'W':
            if self.at(p + 1) == 'o':
                if self.at(p + 2) == 'r':
                    if self.at(p + 3) == 'd':
                        # reached the last letter of 'Word'
                        return ('Word', 'Word', 'type', 'datatype', 4)
        return None

    def scan_word(self):
        start = self.pos
        hit = self.match_reserved(start)
        if hit is not None:
            lexeme, ttype, dkey, category, length = hit
            follow_pos = start + length
            follow = self.at(follow_pos)
            if is_id_char(follow):
                # e.g. "Varying" or "Number2": not the reserved word after
                # all - it is just a longer identifier, so scan it as one.
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
                # the lexeme itself is valid: keep the token, flag it, report
                self.emit(ttype, start, follow_pos, category,
                          concat_pattern(lexeme), flagged=True)
                self.follow_error(what, lexeme, dkey, start, follow_pos)
            self.pos = follow_pos
            return
        self.scan_identifier()

    # ------------------------------------------------------ identifiers --
    def scan_identifier(self):
        start = self.pos
        p = start + 1                       # first char is a letter already
        while is_id_char(self.at(p)):
            p += 1
        length = p - start
        if length > MAX_IDENTIFIER_LENGTH:
            # The first MAX_IDENTIFIER_LENGTH characters become an 'id' and the
            # overflow is reported as an error. Scanning then RESUMES at the cut,
            # so whatever follows is tokenized normally (digits -> int_lit, letters
            # -> id or a reserved word, ...).
            cut = start + MAX_IDENTIFIER_LENGTH
            self.emit("id", start, cut, "identifier", PATTERN_ID)
            self.error(cut,
                       "Identifier exceeds the %d-character limit "
                       "(Identifiers rule 3); the first %d characters were "
                       "tokenized as 'id' and tokenization starts again here."
                       % (MAX_IDENTIFIER_LENGTH, MAX_IDENTIFIER_LENGTH),
                       found=show_char(self.at(cut)),
                       expected="end of identifier (max %d characters)" % MAX_IDENTIFIER_LENGTH,
                       lexeme="", length=1, kind="Invalid identifier")
            self.overflow_end = p
            resume = cut
            while self.at(resume) == '_':   # '_' cannot start a token: it stays inside
                resume += 1                 # the excess already reported above
            self.pos = resume
            return
        lexeme = self.src[start:p]
        follow = self.at(p)
        if d_id(follow):
            self.emit("id", start, p, "identifier", PATTERN_ID)
        else:
            self.emit("id", start, p, "identifier", PATTERN_ID, flagged=True)
            self.follow_error("identifier", lexeme, 'id', start, p)
        self.pos = p

    # ---------------------------------------------------------- numbers --
    def numeric_run_end(self, p):
        """End offset of digits[.digits] starting at p (error recovery)."""
        while is_digit(self.at(p)):
            p += 1
        if self.at(p) == '.':
            if is_digit(self.at(p + 1)):
                p += 1
                while is_digit(self.at(p)):
                    p += 1
        return p

    def scan_number(self):
        start = self.pos
        p = start
        negative = False
        if self.at(p) == '-':                         # (-/lambda) of the int_lit expression
            negative = True
            p += 1
        digit_start = p

        # ---- integer part: zero alone, or (-/lambda) nonzero + digits ----
        if self.at(p) == '0':
            p += 1
            if is_digit(self.at(p)):
                end = self.numeric_run_end(start)
                self.error(start,
                           "Leading zero: an integer must be '0' alone or start "
                           "with a nonzero digit (Literals rule 1).",
                           found="'0' followed by digit '%s'" % self.at(p),
                           expected="'0' alone, or a nonzero first digit",
                           lexeme=self.src[start:end], length=end - start,
                           kind="Invalid number")
                self.pos = end
                return
        else:
            p += 1
            while is_digit(self.at(p)):
                p += 1
        int_end = p
        int_digits = int_end - digit_start
        if int_digits > MAX_INT_DIGITS:
            # tokenize only the first MAX_INT_DIGITS digits as int_lit; the
            # rest is reported as a separate error, not swallowed into one
            cut = digit_start + MAX_INT_DIGITS
            self.emit("int_lit", start, cut, "literal", PATTERN_INT)
            self.error(cut,
                       "Integer literal exceeds the %d-digit limit; the first "
                       "%d digits were tokenized as 'int_lit' and tokenization "
                       "starts again here." % (MAX_INT_DIGITS, MAX_INT_DIGITS),
                       found=show_char(self.at(cut)),
                       expected="end of integer literal (max %d digits)" % MAX_INT_DIGITS,
                       lexeme="", length=1, kind="Invalid number")
            self.pos = cut              # resume scanning AT the error character
            return

        # ---- optional fractional part ------------------------------------
        if self.at(p) == '.':
            p += 1
            if not is_digit(self.at(p)):
                self.error(start,
                           "A float literal needs at least one digit after the "
                           "decimal point (Literals rule 2).",
                           found="%s after '.'" % show_char(self.at(p)),
                           expected="a digit (0-9)",
                           lexeme=self.src[start:p], length=p - start,
                           kind="Invalid number")
                self.pos = p
                return
            frac_start = p
            while is_digit(self.at(p)):
                p += 1
            frac_digits = p - frac_start
            if frac_digits > MAX_FRAC_DIGITS:
                self.error(start,
                           "Fractional part is longer than the %d digits allowed "
                           "(Literals rule 2)." % MAX_FRAC_DIGITS,
                           found="too many fractional digits",
                           expected="at most %d fractional digits" % MAX_FRAC_DIGITS,
                           lexeme=self.src[start:p], length=p - start,
                           kind="Invalid number")
                self.pos = p
                return
            is_float = True
        else:
            is_float = False
            value = int(self.src[start:p])
            if value > INT_MAX or value < -INT_MIN_MAGNITUDE:
                self.error(start,
                           "Integer literal %s is outside Number's range "
                           "(%d to %d, Data Types rule 2)."
                           % (self.src[start:p], -INT_MIN_MAGNITUDE, INT_MAX),
                           found=self.src[start:p],
                           expected="a value from %d to %d" % (-INT_MIN_MAGNITUDE, INT_MAX),
                           lexeme=self.src[start:p], length=p - start,
                           kind="Out-of-range literal")
                self.pos = p
                return

        # ---- what comes right after the number? ---------------------------
        follow = self.at(p)
        if is_id_char(follow):
            q = p
            while is_id_char(self.at(q)):
                q += 1
            self.error(start,
                       "Invalid token '%s': a number cannot be glued to letters "
                       "or underscores, and an identifier cannot start with a "
                       "digit (Identifiers rule 2)." % self.src[start:q],
                       found=show_char(follow) + " right after the number",
                       expected=DELIMS['flo' if is_float else 'int'][1],
                       lexeme=self.src[start:q], length=q - start,
                       kind="Invalid identifier")
            self.pos = q
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

    # ---------------------------------------------------------- strings --
    def scan_string(self):
        start = self.pos
        p = start + 1
        bad = False
        closed = False
        while True:
            c = self.at(p)
            if c == '':                                   # ran off the end
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
            if c == '\\':                                 # escapeseq
                nxt = self.at(p + 1)
                if nxt != '' and nxt in ESCAPE_CHARS:
                    p += 2                                # valid escapeseq: part of the string
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
            if is_control_char(c):                        # U+0000-1F, U+007F
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
            p += 1                                        # ordinary UTF-8 char

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

    # --------------------------------------------------------- comments --
    def scan_comment(self):
        start = self.pos
        if self.at(start + 1) == '(':
            # ---- multi-line comment #( ... )# (does not nest) ----------
            q = start + 2
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
                if c == ')':
                    if self.at(q + 1) == '#':             # first )# closes it
                        break
                if c == '\n':
                    q += 1
                    continue
                if c == '\t':
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
            end = q + 2
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

        # ---- single-line comment # ... end of line -----------------------
        q = start + 1
        bad = False
        while True:
            c = self.at(q)
            if c == '':
                break
            if c == '\n':
                break
            if c == '\t':
                q += 1
                continue
            if is_control_char(c):
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

    # ---------------------------------------- symbols (maximal munch) ----
    def sym(self, lexeme, dkey):
        """Accept symbol `lexeme` at self.pos if its follow char is legal."""
        start = self.pos
        end = start + len(lexeme)
        follow = self.at(end)
        if dkey in ('arco', 'aras', 'minu', 'unar', 'arrw'):
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

    def scan_symbol(self, c):
        p = self.pos
        c1 = self.at(p + 1)

        if c == '+':
            if c1 == '=':
                self.sym('+=', 'arco')
            elif c1 == '+':
                self.sym('++', 'unar')
            else:
                self.sym('+', 'aras')
        elif c == '-':
            if c1 == '=':
                self.sym('-=', 'arco')
            elif c1 == '-':
                self.sym('--', 'unar')
            elif c1 == '>':
                self.sym('->', 'arrw')
            else:
                self.sym('-', 'minu')
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
                self.sym('==', 'aras')
            else:
                self.sym('=', 'aras')
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
                self.sym('!=', 'aras')
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
            self.sym('.', 'strc')
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


def tokenize(source, raise_on_error=True):
    """Convenience wrapper: returns a list of Token, or raises LexicalError."""
    lx = Lexer(source)
    return lx.tokenize(raise_on_error=raise_on_error)


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
        mark = "!" if tok.flagged else " "
        print("%4d:%-3d %s%-12s %r" % (tok.line, tok.col, mark, tok.type, tok.lexeme))
    for err in lexer.errors:
        print("ERROR %d:%d [%s] %s | expected: %s"
              % (err.line, err.col, err.kind, err.message, err.expected))
    print("%d tokens, %d errors" % (
        len([t for t in lexer.tokens if t.type != "newline"]), len(lexer.errors)))
    return 1 if lexer.errors else 0


if __name__ == "__main__":
    path = sys.argv[2] if len(sys.argv) > 2 else "-"
    sys.exit(run_cli(path))