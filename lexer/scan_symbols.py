"""
scan_symbols.py - reserved symbols (TD B, states 210-274), written as one
if / elif branch per state.

Longest match: while the next character has an arrow from the current state
the symbol continues (+ then + gives ++), even if that character is also in
the delimiter set.  Then the delimiter arrow into the final state is checked.

253 (~) also has arrows on zero -> 335 and nonzero -> 337 (a negative
literal); the main loop sends "~digit" to scan_numbers, so here 253 only
takes its neg_delim arrow.
"""

from .definitions import DELIM
from .emit import accept_symbol
from . import errors as E


def scan_symbol(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:        # start
            if c == "+":
                state = 210
            elif c == "-":
                state = 216
            elif c == "*":
                state = 224
            elif c == "/":
                state = 228
            elif c == "%":
                state = 232
            elif c == "^":
                state = 236
            elif c == "=":
                state = 238
            elif c == "!":
                state = 242
            elif c == ">":
                state = 245
            elif c == "<":
                state = 249
            elif c == "~":
                state = 253
            elif c == "(":
                state = 255
            elif c == ")":
                state = 257
            elif c == "[":
                state = 259
            elif c == "]":
                state = 261
            elif c == "{":
                state = 263
            elif c == "}":
                state = 265
            elif c == ":":
                state = 267
            elif c == ";":
                state = 269
            elif c == ".":
                state = 271
            elif c == ",":
                state = 273
            else:
                return
        elif state == 210:    # '+'
            if c == "=":
                state = 212
            elif c == "+":
                state = 214
            elif c in DELIM["op_plus_delim"]:
                accept_symbol(src, tokens, start, path, 211, "+")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "+", "op_plus_delim", 210))
                return
        elif state == 212:    # '+='
            if c in DELIM["op_string_delim"]:
                accept_symbol(src, tokens, start, path, 213, "+=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "+=", "op_string_delim", 212))
                return
        elif state == 214:    # '++'
            if c in DELIM["unary_delim"]:
                accept_symbol(src, tokens, start, path, 215, "++")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "++", "unary_delim", 214))
                return
        elif state == 216:    # '-'
            if c == "=":
                state = 218
            elif c == "-":
                state = 220
            elif c == ">":
                state = 222
            elif c in DELIM["op_minus_delim"]:
                accept_symbol(src, tokens, start, path, 217, "-")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "-", "op_minus_delim", 216))
                return
        elif state == 218:    # '-='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 219, "-=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "-=", "op_delim", 218))
                return
        elif state == 220:    # '--'
            if c in DELIM["unary_delim"]:
                accept_symbol(src, tokens, start, path, 221, "--")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "--", "unary_delim", 220))
                return
        elif state == 222:    # '->'
            if c in DELIM["arrow_delim"]:
                accept_symbol(src, tokens, start, path, 223, "->")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "->", "arrow_delim", 222))
                return
        elif state == 224:    # '*'
            if c == "=":
                state = 226
            elif c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 225, "*")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "*", "op_delim", 224))
                return
        elif state == 226:    # '*='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 227, "*=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "*=", "op_delim", 226))
                return
        elif state == 228:    # '/'
            if c == "=":
                state = 230
            elif c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 229, "/")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "/", "op_delim", 228))
                return
        elif state == 230:    # '/='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 231, "/=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "/=", "op_delim", 230))
                return
        elif state == 232:    # '%'
            if c == "=":
                state = 234
            elif c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 233, "%")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "%", "op_delim", 232))
                return
        elif state == 234:    # '%='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 235, "%=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "%=", "op_delim", 234))
                return
        elif state == 236:    # '^'
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 237, "^")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "^", "op_delim", 236))
                return
        elif state == 238:    # '='
            if c == "=":
                state = 240
            elif c in DELIM["op_string_delim"]:
                accept_symbol(src, tokens, start, path, 239, "=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "=", "op_string_delim", 238))
                return
        elif state == 240:    # '=='
            if c in DELIM["op_string_delim"]:
                accept_symbol(src, tokens, start, path, 241, "==")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "==", "op_string_delim", 240))
                return
        elif state == 242:    # '!'
            if c == "=":
                state = 243
            else:
                errors.append(E.lone_bang(src, start))   # '!' needs '='
                return
        elif state == 243:    # '!='
            if c in DELIM["op_string_delim"]:
                accept_symbol(src, tokens, start, path, 244, "!=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "!=", "op_string_delim", 243))
                return
        elif state == 245:    # '>'
            if c == "=":
                state = 247
            elif c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 246, ">")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ">", "op_delim", 245))
                return
        elif state == 247:    # '>='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 248, ">=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ">=", "op_delim", 247))
                return
        elif state == 249:    # '<'
            if c == "=":
                state = 251
            elif c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 250, "<")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "<", "op_delim", 249))
                return
        elif state == 251:    # '<='
            if c in DELIM["op_delim"]:
                accept_symbol(src, tokens, start, path, 252, "<=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "<=", "op_delim", 251))
                return
        elif state == 253:    # '~'
            if c in DELIM["neg_delim"]:
                accept_symbol(src, tokens, start, path, 254, "~")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "~", "neg_delim", 253))
                return
        elif state == 255:    # '('
            if c in DELIM["paren_open_delim"]:
                accept_symbol(src, tokens, start, path, 256, "(")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "(", "paren_open_delim", 255))
                return
        elif state == 257:    # ')'
            if c in DELIM["val_delim"]:
                accept_symbol(src, tokens, start, path, 258, ")")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ")", "val_delim", 257))
                return
        elif state == 259:    # '['
            if c in DELIM["bracket_open_delim"]:
                accept_symbol(src, tokens, start, path, 260, "[")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "[", "bracket_open_delim", 259))
                return
        elif state == 261:    # ']'
            if c in DELIM["clsq_delim"]:
                accept_symbol(src, tokens, start, path, 262, "]")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "]", "clsq_delim", 261))
                return
        elif state == 263:    # '{'
            if c in DELIM["brace_open_delim"]:
                accept_symbol(src, tokens, start, path, 264, "{")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "{", "brace_open_delim", 263))
                return
        elif state == 265:    # '}'
            if c in DELIM["brace_close_delim"]:
                accept_symbol(src, tokens, start, path, 266, "}")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "}", "brace_close_delim", 265))
                return
        elif state == 267:    # ':'
            if c in DELIM["colon_delim"]:
                accept_symbol(src, tokens, start, path, 268, ":")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ":", "colon_delim", 267))
                return
        elif state == 269:    # ';'
            if c in DELIM["semi_delim"]:
                accept_symbol(src, tokens, start, path, 270, ";")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ";", "semi_delim", 269))
                return
        elif state == 271:    # '.'
            if c in DELIM["dot_delim"]:
                accept_symbol(src, tokens, start, path, 272, ".")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ".", "dot_delim", 271))
                return
        elif state == 273:    # ','
            if c in DELIM["comma_delim"]:
                accept_symbol(src, tokens, start, path, 274, ",")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ",", "comma_delim", 273))
                return
        src.advance()
        path.append(state)
