"""
errors.py - LexicalError and every lexical error message.

A LexicalError records where the diagram got stuck (`state`), the character
that caused it (`found`), what the paper allows there (`expected`), and the
invalid lexeme.  The lexer collects them in a list and keeps scanning, so one
run reports every error.
"""

from .definitions import DELIM_TEXT


class LexicalError(Exception):
    def __init__(self, message, line, col, found="", expected="", lexeme="",
                 kind="Lexical error", state=None):
        super().__init__("%d:%d %s" % (line, col, message))
        self.message = message
        self.line = line
        self.col = col
        self.found = found
        self.expected = expected
        self.lexeme = lexeme
        self.kind = kind
        self.state = state
        self.errors = [self]


def show_char(c):
    """Readable name for a character in an error message."""
    if c == "":
        return "end of file"
    names = {"\n": "newline", "\t": "tab", " ": "space"}
    if c in names:
        return names[c]
    if ord(c) < 0x20 or ord(c) == 0x7F:
        return "control character U+%04X" % ord(c)
    return "'%s'" % c


def _err(src, pos, message, kind, state, found="", expected="", lexeme=""):
    line, col = src.loc(pos)
    return LexicalError(message, line, col, found, expected, lexeme, kind, state)


# --- the messages ---------------------------------------------------------------

def invalid_delimiter(src, start, follow_pos, what, lexeme, delim, state,
                      expected=None):
    c = src.text[follow_pos] if follow_pos < src.n else ""
    sline, scol = src.loc(start)
    msg = ("%s '%s' (starting at %d:%d) is followed by %s, which is not in "
           "its delimiter set %s." % (what, lexeme, sline, scol,
                                      show_char(c), delim))
    if expected is None:
        expected = DELIM_TEXT[delim]
    return _err(src, follow_pos, msg, "Invalid delimiter", state,
                show_char(c), expected, lexeme)


def illegal_character(src, pos):
    c = src.text[pos]
    msg = ("%s does not start any token of LIME (no arrow leaves state 0 "
           "with it)." % show_char(c))
    return _err(src, pos, msg, "Illegal character", 0, show_char(c),
                "a letter, a digit, \", #, whitespace or a reserved symbol", c)


def lone_bang(src, start):
    c = src.text[start + 1] if start + 1 < src.n else ""
    msg = ("'!' must be followed by '=' (state 248 has no other arrow); "
           "found %s. Use Not for logical negation." % show_char(c))
    return _err(src, start, msg, "Invalid symbol", 248, show_char(c), "=",
                "!")


def underscore_start(src, pos, lexeme):
    msg = ("An identifier cannot start with an underscore; the first "
           "character must be a letter (Identifiers Rules 2 and 4). No arrow "
           "leaves state 0 on '_'; scanning restarts at the next character.")
    return _err(src, pos, msg, "Invalid identifier", 0, "'_'", "a letter",
                lexeme)


def identifier_too_long(src, start, lexeme):
    # 30th character (state 329) followed by a 31st: not in delim_id.
    return invalid_delimiter(src, start, src.pos, "Identifier", lexeme,
                             "delim_id", 329)


def leading_zero(src, start, lexeme):
    # 0 (state 331) followed by another digit: not in delim_int.
    return invalid_delimiter(src, start, src.pos, "Number literal", lexeme,
                             "delim_int", 331,
                             DELIM_TEXT["delim_int"] + ", or a period")


def too_many_int_digits(src, start, lexeme):
    # 19th digit (state 369) followed by a 20th: not in delim_int.
    return invalid_delimiter(src, start, src.pos, "Number literal", lexeme,
                             "delim_int", 369,
                             DELIM_TEXT["delim_int"] + ", or a period")


def too_many_frac_digits(src, start, lexeme):
    # 17th fractional digit (state 404) followed by an 18th: not in delim_flo.
    return invalid_delimiter(src, start, src.pos, "Rational literal", lexeme,
                             "delim_flo", 404)


def missing_fraction(src, start, follow_pos, lexeme):
    c = src.text[follow_pos] if follow_pos < src.n else ""
    msg = ("A Rational literal needs at least one digit after the decimal "
           "point (Literals Rule 2); state 371 has no arrow on %s."
           % show_char(c))
    return _err(src, follow_pos, msg, "Invalid rational literal", 371,
                show_char(c), "a digit", lexeme)


def invalid_escape(src, start, pos, lexeme):
    c = src.peek()
    msg = ("Invalid escape sequence: the backslash is followed by %s; Word "
           "literals support only \\n, \\t, \\\\ and \\\" (Literals Rule 4). "
           "Scanning restarts at that character." % show_char(c))
    return _err(src, pos, msg, "Invalid escape sequence", 406, show_char(c),
                "\\n, \\t, \\\\, \\\"", lexeme)


def bad_string_char(src, start, pos, lexeme):
    c = src.text[pos]
    msg = ("%s is not allowed inside a Word literal (utf8_str); the diagram "
           "has no arrow out of state 406 on it. Scanning restarts at that "
           "character." % show_char(c))
    return _err(src, pos, msg, "Invalid character in Word", 406,
                show_char(c), "utf8_str or an escape sequence", lexeme)


def unclosed_string(src, start, lexeme):
    msg = ("Word literal is never closed: a newline or the end of the file "
           "was reached before the closing \" (state 406).")
    return _err(src, start, msg, "Unclosed Word literal", 406, "", '"',
                lexeme)


def bad_comment_char(src, start, pos, state, lexeme):
    c = src.text[pos]
    msg = ("%s is not allowed in a comment; tab is the only control character "
           "allowed (Comments Rules 1 and 2). The diagram has no arrow out of "
           "state %d on it; scanning restarts at that character."
           % (show_char(c), state))
    return _err(src, pos, msg, "Invalid character in comment", state,
                show_char(c), "utf8_comm", lexeme)


def unclosed_comment(src, start, lexeme):
    msg = ("Multi-line comment is never closed: the end of the file was "
           "reached before )# (Comments Rule 2).")
    return _err(src, start, msg, "Unclosed comment", 412, "", ")#",
                lexeme[:40] + ("..." if len(lexeme) > 40 else ""))


def after_multi_comment(src, pos, lexeme):
    c = src.text[pos] if pos < src.n else ""
    msg = ("Only whitespace may follow )# on the same line (Comments Rules 2 "
           "and 6), but %s was found." % show_char(c))
    return _err(src, pos, msg, "Invalid delimiter", 414, show_char(c),
                DELIM_TEXT["delim_muco"], lexeme[-20:])