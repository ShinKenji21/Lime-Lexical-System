"""
scan_comments.py - single_comm and multi_comm (TD F, states 390-396), one
if / elif branch per state.

0 --#--> 390
  390 --sico_delim--> 392*                     empty comment: # then newline/EOF
  390 --utf8_no_oppa--> 391 --utf8_comm--> 391 --sico_delim--> 392*
  390 --(--> 393 --utf8_comm/newline--> 393 --)--> 394 --#--> 395
       395 --muco_delim--> 396*

At 394 a ) that is not followed by # is comment text (Comments Rule 10), so
394 goes back to 393 (or stays at 394 on another ')'); the comment ends at the
first )# (Comments Rule 8).  After )# only whitespace may follow on the same
line (Comments Rule 9).
"""

from .definitions import DELIM, utf8_comm, utf8_no_oppa, space, tab
from .tokens import make_token, SINGLE_COMM, MULTI_COMM, CAT_COMMENT
from . import errors as E


def scan_comment(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:                              # start
            if c == "#":
                state = 390
            else:
                return
        elif state == 390:                          # '#'
            if c in DELIM["sico_delim"]:            # empty comment
                tokens.append(make_token(src, SINGLE_COMM, start, CAT_COMMENT,
                                         392, path + [392]))
                return
            elif c == "(":
                state = 393
            elif utf8_no_oppa(c):
                state = 391
            else:
                errors.append(E.bad_comment_char(src, start, src.pos, 390, src.slice(start)))
                return                              # back to state 0 at this character
        elif state == 391:                          # single-line comment text
            if c in DELIM["sico_delim"]:
                tokens.append(make_token(src, SINGLE_COMM, start,
                                         CAT_COMMENT, 392, path + [392]))
                return
            elif utf8_comm(c):
                state = 391
            else:
                errors.append(E.bad_comment_char(src, start, src.pos, 391, src.slice(start)))
                return                              # back to state 0 at this character
        elif state == 393:                          # multi-line comment text
            if c == ")":
                state = 394
            elif utf8_comm(c) or c == "\n":
                state = 393
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            else:
                errors.append(E.bad_comment_char(src, start, src.pos, 393, src.slice(start)))
                return                              # back to state 0 at this character
        elif state == 394:                          # ')' read
            if c == "#":
                state = 395
            elif c == ")":
                state = 394
            elif utf8_comm(c) or c == "\n":
                state = 393                         # the ) was comment text
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            else:
                errors.append(E.bad_comment_char(src, start, src.pos, 394, src.slice(start)))
                return                              # back to state 0 at this character
        elif state == 395:                          # ')#' read
            if c not in DELIM["muco_delim"]:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Multi-line comment",
                                                  src.slice(start)[-20:], "muco_delim", 395))
                return
            # 395 --muco_delim--> 396*.  Code cannot follow )# on the same
            # line (Comments Rule 9): only spaces / tabs until newline or EOF.
            p = src.pos
            while p < src.n and (src.text[p] in space or src.text[p] in tab):
                p += 1
            if p < src.n and src.text[p] != "\n":
                errors.append(E.after_multi_comment(src, p, src.slice(start)))
                return
            tokens.append(make_token(src, MULTI_COMM, start, CAT_COMMENT,
                                     396, path + [396]))
            return
        src.advance()
        if path[-1] != state:       # loops (391 -> 391) are shown once
            path.append(state)
