"""
scan_symbols.py - reserved symbols (TD B, states 206-270), written as one
if / elif branch per state.

Longest match: while the next character has an arrow from the current state
the symbol continues (+ then + gives ++), even if that character is also in
the delimiter set.  Then the delimiter arrow into the final state is checked.

220 (~) also has arrows on zero -> 331 and nonzero -> 333 (a negative
literal); the main loop sends "~digit" to scan_numbers, so here 220 only
takes its delim_neg arrow.
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
                state = 206
            elif c == "-":
                state = 212
            elif c == "~":
                state = 220
            elif c == "*":
                state = 222
            elif c == "/":
                state = 226
            elif c == "%":
                state = 230
            elif c == "^":
                state = 234
            elif c == "=":
                state = 236
            elif c == ">":
                state = 240
            elif c == "<":
                state = 244
            elif c == "!":
                state = 248
            elif c == ")":
                state = 251
            elif c == "(":
                state = 253
            elif c == "[":
                state = 255
            elif c == "]":
                state = 257
            elif c == "{":
                state = 259
            elif c == "}":
                state = 261
            elif c == ":":
                state = 263
            elif c == ";":
                state = 265
            elif c == ".":
                state = 267
            elif c == ",":
                state = 269
            else:
                return
        elif state == 206:    # '+'
            if c == "=":
                state = 208
            elif c == "+":
                state = 210
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 207, "+")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "+", "delim_arco", 206))
                return
        elif state == 208:    # '+='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 209, "+=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "+=", "delim_arco", 208))
                return
        elif state == 210:    # '++'
            if c in DELIM["delim_unar"]:
                accept_symbol(src, tokens, start, path, 211, "++")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "++", "delim_unar", 210))
                return
        elif state == 212:    # '-'
            if c == "=":
                state = 214
            elif c == "-":
                state = 216
            elif c == ">":
                state = 218
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 213, "-")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "-", "delim_arco", 212))
                return
        elif state == 214:    # '-='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 215, "-=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "-=", "delim_arco", 214))
                return
        elif state == 216:    # '--'
            if c in DELIM["delim_unar"]:
                accept_symbol(src, tokens, start, path, 217, "--")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "--", "delim_unar", 216))
                return
        elif state == 218:    # '->'
            if c in DELIM["delim_arrw"]:
                accept_symbol(src, tokens, start, path, 219, "->")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "->", "delim_arrw", 218))
                return
        elif state == 220:    # '~'
            if c in DELIM["delim_neg"]:
                accept_symbol(src, tokens, start, path, 221, "~")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "~", "delim_neg", 220))
                return
        elif state == 222:    # '*'
            if c == "=":
                state = 224
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 223, "*")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "*", "delim_arco", 222))
                return
        elif state == 224:    # '*='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 225, "*=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "*=", "delim_arco", 224))
                return
        elif state == 226:    # '/'
            if c == "=":
                state = 228
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 227, "/")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "/", "delim_arco", 226))
                return
        elif state == 228:    # '/='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 229, "/=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "/=", "delim_arco", 228))
                return
        elif state == 230:    # '%'
            if c == "=":
                state = 232
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 231, "%")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "%", "delim_arco", 230))
                return
        elif state == 232:    # '%='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 233, "%=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "%=", "delim_arco", 232))
                return
        elif state == 234:    # '^'
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 235, "^")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "^", "delim_arco", 234))
                return
        elif state == 236:    # '='
            if c == "=":
                state = 238
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 237, "=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "=", "delim_arco", 236))
                return
        elif state == 238:    # '=='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 239, "==")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "==", "delim_arco", 238))
                return
        elif state == 240:    # '>'
            if c == "=":
                state = 242
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 241, ">")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ">", "delim_arco", 240))
                return
        elif state == 242:    # '>='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 243, ">=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ">=", "delim_arco", 242))
                return
        elif state == 244:    # '<'
            if c == "=":
                state = 246
            elif c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 245, "<")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "<", "delim_arco", 244))
                return
        elif state == 246:    # '<='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 247, "<=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "<=", "delim_arco", 246))
                return
        elif state == 248:    # '!'
            if c == "=":
                state = 249
            else:
                errors.append(E.lone_bang(src, start))   # '!' needs '='
                return
        elif state == 249:    # '!='
            if c in DELIM["delim_arco"]:
                accept_symbol(src, tokens, start, path, 250, "!=")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "!=", "delim_arco", 249))
                return
        elif state == 251:    # ')'
            if c in DELIM["delim_clpa"]:
                accept_symbol(src, tokens, start, path, 252, ")")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ")", "delim_clpa", 251))
                return
        elif state == 253:    # '('
            if c in DELIM["delim_pare"]:
                accept_symbol(src, tokens, start, path, 254, "(")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "(", "delim_pare", 253))
                return
        elif state == 255:    # '['
            if c in DELIM["delim_squa"]:
                accept_symbol(src, tokens, start, path, 256, "[")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "[", "delim_squa", 255))
                return
        elif state == 257:    # ']'
            if c in DELIM["delim_clsq"]:
                accept_symbol(src, tokens, start, path, 258, "]")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "]", "delim_clsq", 257))
                return
        elif state == 259:    # '{'
            if c in DELIM["delim_brac"]:
                accept_symbol(src, tokens, start, path, 260, "{")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "{", "delim_brac", 259))
                return
        elif state == 261:    # '}'
            if c in DELIM["delim_clbr"]:
                accept_symbol(src, tokens, start, path, 262, "}")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  "}", "delim_clbr", 261))
                return
        elif state == 263:    # ':'
            if c in DELIM["delim_colo"]:
                accept_symbol(src, tokens, start, path, 264, ":")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ":", "delim_colo", 263))
                return
        elif state == 265:    # ';'
            if c in DELIM["delim_semi"]:
                accept_symbol(src, tokens, start, path, 266, ";")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ";", "delim_semi", 265))
                return
        elif state == 267:    # '.'
            if c in DELIM["delim_dot"]:
                accept_symbol(src, tokens, start, path, 268, ".")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ".", "delim_dot", 267))
                return
        elif state == 269:    # ','
            if c in DELIM["delim_coma"]:
                accept_symbol(src, tokens, start, path, 270, ",")
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Symbol",
                                                  ",", "delim_coma", 269))
                return
        src.advance()
        path.append(state)
