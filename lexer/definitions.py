"""
definitions.py - the REGULAR DEFINITIONS section of the LIME paper (pp. 81-84),
row for row.

Finite character sets are Python sets of one-character strings.  The three
"any UTF-8 character except ..." definitions (utf8_str, utf8_comm,
utf8_no_oppa) are infinite, so they are written as functions that answer
"is c in this set?".

EOF is represented by the empty string "" (Source.peek() returns "" past the
end of the file), so a delimiter set that allows EOF simply contains "".

Every delim_* set lives in one dict, DELIM, so the scanners look a delimiter
up by its name from the transition diagram, e.g. DELIM["delim_int"].
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


def _is_control(c):
    # U+0000 to U+001F and U+007F (Delete)
    return c != "" and (ord(c) <= 0x1F or ord(c) == 0x7F)


def utf8_str(c):
    """Any UTF-8 character except U+0000-U+001F, U+0022 ("), U+005C (\\) and
    U+007F.  Tab (U+0009) is the only control character included."""
    if c == "":
        return False
    if c == "\t":
        return True
    return not _is_control(c) and c != '"' and c != "\\"


def utf8_comm(c):
    """Any UTF-8 character except U+0000-U+001F and U+007F.  Tab is the only
    control character included."""
    if c == "":
        return False
    if c == "\t":
        return True
    return not _is_control(c)


def utf8_no_oppa(c):
    """utf8_comm without U+0028 (opening parenthesis)."""
    return utf8_comm(c) and c != "("


backslash = "\\"
newline = {"\n"}          # LF; CR LF is turned into one LF by Source
tab = {"\t"}
newline_esq = "n"         # the character that follows the backslash in \n
tab_esq = "t"             # \t
quote_esq = '"'           # \"
backslash_esq = "\\"      # \\
escapeseq = {newline_esq, tab_esq, quote_esq, backslash_esq}
space = {" "}
whitespace = space | tab
arith_op = {"+", "-", "*", "/", "%", "^"}
compare_op = {">", "<"}
compare_etc = {"==", ">=", "<=", "!="}
assign_op = {"="}
assign_etc = {"+=", "-=", "*=", "/=", "%="}
unary_op = {"++", "--"}
ret_typ = {"->"}
multi_comm = {"#(", ")#"}
comma = {","}
semi_colon = {";"}
period = {"."}
null = ""                 # λ
eof = {EOF}

# Characters that can continue an identifier (used to decide whether a fully
# spelled reserved word is really the start of a longer identifier).
id_chars = lets_nums | underscore

# --- delimiters ---------------------------------------------------------------
_NW = newline | whitespace
_OPS = {"+", "-", "*", "/", "%", "^", "=", ">", "<", "!"}

DELIM = {
    "delim_type": _NW | comma | {"="} | semi_colon | {")", "{", "["},
    "delim_blan": _NW | {"{"},
    "delim_ctrl": _NW | {"("},
    "delim_taun": _NW | {"{"},
    "delim_reup": _NW | semi_colon | {"}"},
    "delim_prod": _NW | semi_colon | {"(", "}"},
    "delim_unar": letters | _NW | comma | semi_colon | {")", "]", "}"} | _OPS,
    "delim_coma": lets_nums | _NW | {"+", "-", "~", '"', "(", "["},
    "delim_pare": lets_nums | _NW | semi_colon | {"+", "-", "~", '"', "(", ")"},
    "delim_clpa": _NW | comma | semi_colon | {")", "]", "{", "}"} | _OPS,
    "delim_clsq": _NW | comma | semi_colon | {")", "[", "]", "{", "}"} | _OPS,
    "delim_clbr": _NW | {"#", "}"} | eof,
    "delim_squa": lets_nums | _NW | {"+", "-", "~", "(", "[", "]", '"'},
    "delim_brac": letters | _NW | {"+", "-", "~", "}", "#"},
    "delim_colo": {"N", "R", "W", "T"} | _NW,
    "delim_arrw": {"B", "N", "R", "W", "T"} | _NW,
    "delim_semi": lets_nums | _NW | semi_colon
                  | {"+", "-", "~", "(", ")", "}", "#", '"'} | eof,
    "delim_muco": _NW | eof,
    "delim_sico": newline | eof,
    "delim_id": _NW | comma | semi_colon | period
                | {")", "]", "{", "}", "(", "[", ":"} | _OPS,
    "delim_str": _NW | comma | semi_colon | {")", "]", "{", "}"} | _OPS,
    "delim_int": _NW | comma | semi_colon | {")", "]", "{", "}"} | _OPS,
    "delim_flo": _NW | comma | semi_colon | {")", "]", "{", "}"} | _OPS,
    "delim_bool": _NW | comma | semi_colon | {")", "]", "{", "}"} | _OPS,
    "delim_neg": letters | {"(", "~"},
    "delim_arco": lets_nums | _NW | {"~", "(", '"', "+", "-"},
    "delim_decl": _NW,
    "delim_bask": _NW | {"["},
    "delim_logi": _NW | {"("},
    "delim_func": _NW | {"("},
    "delim_dot": letters,
}

# The same rows as text, used for the "Expected:" line of an error message.
_NW_T = "newline, whitespace"
_OPS_T = "+, -, *, /, %, ^, =, >, <, !"
DELIM_TEXT = {
    "delim_type": _NW_T + ", comma, =, ;, ), {, [",
    "delim_blan": _NW_T + ", {",
    "delim_ctrl": _NW_T + ", (",
    "delim_taun": _NW_T + ", {",
    "delim_reup": _NW_T + ", ;, }",
    "delim_prod": _NW_T + ", ;, (, }",
    "delim_unar": "letters, " + _NW_T + ", comma, ;, ), ], }, " + _OPS_T,
    "delim_coma": "letters, numbers, " + _NW_T + ', +, -, ~, ", (, [',
    "delim_pare": "letters, numbers, " + _NW_T + ', ;, +, -, ~, ", (, )',
    "delim_clpa": _NW_T + ", comma, ;, ), ], {, }, " + _OPS_T,
    "delim_clsq": _NW_T + ", comma, ;, ), [, ], {, }, " + _OPS_T,
    "delim_clbr": _NW_T + ", #, }, EOF",
    "delim_squa": "letters, numbers, " + _NW_T + ', +, -, ~, (, [, ], "',
    "delim_brac": "letters, " + _NW_T + ", +, -, ~, }, #",
    "delim_colo": "N, R, W, T, " + _NW_T,
    "delim_arrw": "B, N, R, W, T, " + _NW_T,
    "delim_semi": "letters, numbers, " + _NW_T + ', ;, +, -, ~, (, ), }, #, ", EOF',
    "delim_muco": _NW_T + ", EOF",
    "delim_sico": "newline, EOF",
    "delim_id": _NW_T + ", comma, ;, period, ), ], {, }, (, [, :, " + _OPS_T,
    "delim_str": _NW_T + ", comma, ;, ), ], {, }, " + _OPS_T,
    "delim_int": _NW_T + ", comma, ;, ), ], {, }, " + _OPS_T,
    "delim_flo": _NW_T + ", comma, ;, ), ], {, }, " + _OPS_T,
    "delim_bool": _NW_T + ", comma, ;, ), ], {, }, " + _OPS_T,
    "delim_neg": "letters, (, ~",
    "delim_arco": "letters, numbers, " + _NW_T + ', ~, (, ", +, -',
    "delim_decl": _NW_T,
    "delim_bask": _NW_T + ", [",
    "delim_logi": _NW_T + ", (",
    "delim_func": _NW_T + ", (",
    "delim_dot": "letters",
}


def in_delim(name, c):
    """True when character c (or "" for EOF) is in the delimiter set `name`."""
    return c in DELIM[name]
