"""
definitions.py - the REGULAR DEFINITIONS section of the LIME paper (pp. 98-100),
row for row.

Finite character sets are Python sets of one-character strings.  The three
"any UTF-8 character except ..." definitions (utf8_str, utf8_comm,
utf8_no_oppa) are infinite, so they are written as functions that answer
"is c in this set?".

EOF is represented by the empty string "" (Source.peek() returns "" past the
end of the file), so a delimiter set that allows EOF simply contains "".

Every *_delim set lives in one dict, DELIM, so the scanners look a delimiter
up by its name from the transition diagram, e.g. DELIM["val_delim"].
"""

EOF = ""

# --- character classes -------------------------------------------------------
lowercase = set("abcdefghijklmnñopqrstuvwxyz")
uppercase = set("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
letters = lowercase | uppercase
zero = {"0"}
nonzero = set("123456789")
numbers = zero | nonzero
lets_nums = letters | numbers
underscore = {"_"}

space = {" "}
tab = {"\t"}
newline = {"\n"}          # LF; CR LF is turned into one LF by Source
whitespace = space | tab | newline

esc_char = {"n", "t", '"', "\\"}   # the character after \ in \n \t \" \\
backslash = "\\"
period = {"."}


def _is_control(c):
    # U+0000 to U+001F and U+007F (Delete)
    return c != "" and (ord(c) <= 0x1F or ord(c) == 0x7F)


def utf8_str(c):
    """Any UTF-8 character except U+0000-U+001F, '"' (U+0022), '\\' and
    Delete (U+007F).  Tab is the only control character included."""
    if c == "":
        return False
    if c == "\t":
        return True
    return not _is_control(c) and c != '"' and c != "\\"


def utf8_comm(c):
    """Any UTF-8 character except U+0000-U+001F and Delete (U+007F).  Tab is
    the only control character included."""
    if c == "":
        return False
    if c == "\t":
        return True
    return not _is_control(c)


def utf8_no_oppa(c):
    """utf8_comm except '('."""
    return utf8_comm(c) and c != "("


arith_op = {"+", "-", "*", "/", "%", "^"}
rel_op = {"=", "!", ">", "<"}
eof = {EOF}

# Characters that can continue an identifier (lets_nums / underscore).  Used to
# decide whether a fully spelled reserved word is really the start of a longer
# identifier (Tester, Varying).
id_chars = lets_nums | underscore

# --- delimiters ------------------------------------------------------------------
token_delim = whitespace
stmt_delim = token_delim | {";"}
op_delim = token_delim | lets_nums | {"(", "~", "+", "-"}
op_string_delim = op_delim | {'"'}
val_delim = stmt_delim | arith_op | rel_op | {",", ")", "]", "{"}
brace_open_delim = token_delim | letters | {"+", "-", "}", "#"}

DELIM = {
    "token_delim": token_delim,
    "stmt_delim": stmt_delim,
    "method_delim": token_delim | {"("},
    "block_delim": token_delim | {"{"},
    "bask_delim": token_delim | {"["},
    "prod_delim": stmt_delim | {"("},
    "type_delim": stmt_delim | {",", "=", ")", "[", "{"},
    "val_delim": val_delim,
    "id_delim": val_delim | {".", "(", "[", ":"},
    "clsq_delim": val_delim | {"["},
    "unary_delim": stmt_delim | letters | arith_op | rel_op | {",", ")", "]"},
    "op_delim": op_delim,
    "op_string_delim": op_string_delim,
    "op_plus_delim": token_delim | lets_nums | {"(", "~", '"', "-"},
    "op_minus_delim": token_delim | lets_nums | {"(", "~", "+"},
    "comma_delim": op_string_delim | {"["},
    "paren_open_delim": op_string_delim | {")", ";"},
    "bracket_open_delim": op_string_delim | {"[", "]"},
    "brace_open_delim": brace_open_delim,
    "brace_close_delim": brace_open_delim | eof,
    "semi_delim": token_delim | lets_nums
                  | {";", "+", "-", "~", "(", ")", "}", "#", '"'} | eof,
    "colon_delim": token_delim | letters,
    "arrow_delim": token_delim | {"B", "N", "R", "W", "T"},
    "dot_delim": letters,
    "neg_delim": letters | {"(", "~"},
    "sico_delim": newline | eof,
    "muco_delim": token_delim | eof,
}

# The same rows as text, used for the "Expected:" line of an error message.
_WS = "whitespace (space, tab, newline)"
_ARITH = "+, -, *, /, %, ^"
_REL = "=, !, >, <"
_VAL = _WS + ", ;, " + _ARITH + ", " + _REL + ", comma, ), ], {"
_OP = _WS + ", letters, numbers, (, ~, +, -"
DELIM_TEXT = {
    "token_delim": _WS,
    "stmt_delim": _WS + ", ;",
    "method_delim": _WS + ", (",
    "block_delim": _WS + ", {",
    "bask_delim": _WS + ", [",
    "prod_delim": _WS + ", ;, (",
    "type_delim": _WS + ", ;, comma, =, ), [, {",
    "val_delim": _VAL,
    "id_delim": _VAL + ", ., (, [, :",
    "clsq_delim": _VAL + ", [",
    "unary_delim": _WS + ", ;, letters, " + _ARITH + ", " + _REL + ", comma, ), ]",
    "op_delim": _OP,
    "op_string_delim": _OP + ', "',
    "op_plus_delim": _WS + ', letters, numbers, (, ~, ", -',
    "op_minus_delim": _WS + ", letters, numbers, (, ~, +",
    "comma_delim": _OP + ', ", [',
    "paren_open_delim": _OP + ', ", ), ;',
    "bracket_open_delim": _OP + ', ", [, ]',
    "brace_open_delim": _WS + ", letters, +, -, }, #",
    "brace_close_delim": _WS + ", letters, +, -, }, #, EOF",
    "semi_delim": _WS + ', letters, numbers, ;, +, -, ~, (, ), }, #, ", EOF',
    "colon_delim": _WS + ", letters",
    "arrow_delim": _WS + ", B, N, R, W, T",
    "dot_delim": "letters",
    "neg_delim": "letters, (, ~",
    "sico_delim": "newline, EOF",
    "muco_delim": _WS + ", EOF",
}


def in_delim(name, c):
    """True when character c (or "" for EOF) is in the delimiter set `name`."""
    return c in DELIM[name]
