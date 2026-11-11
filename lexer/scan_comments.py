"""
scan_comments.py - single_comm and multi_comm (TD C, states 417-423), one
if / elif branch per state.

0 --#--> 417
  417 --delim_sico--> 419*                     empty comment: # then newline/EOF
  417 --utf8_no_oppa--> 418 --utf8_comm--> 418 --delim_sico--> 419*
  417 --(--> 420 --utf8_comm/newline--> 420 --)--> 421 --#--> 422
       422 --delim_muco--> 423*

At 421 a ) that is not followed by # is comment text (Comments Rule 7), so
421 goes back to 420 (or stays at 421 on another ')').
"""

from .definitions import DELIM, utf8_comm, utf8_no_oppa, whitespace
from .tokens import make_token, SINGLE_COMM, MULTI_COMM, CAT_COMMENT
from . import errors as E


def scan_comment(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    bad = False                 # an invalid control character was reported
    while True:
        c = src.peek()
        if state == 0:                              # start
            if c == "#":
                state = 417
            else:
                return
        elif state == 417:                          # '#'
            if c in DELIM["delim_sico"]:            # empty comment
                tokens.append(make_token(src, SINGLE_COMM, start, CAT_COMMENT,
                                         419, path + [419]))
                return
            elif c == "(":
                state = 420
            elif utf8_no_oppa(c):
                state = 418
            else:
                errors.append(E.bad_comment_char(src, src.pos, 417))
                bad = True
                state = 418
        elif state == 418:                          # single-line comment text
            if c in DELIM["delim_sico"]:
                if not bad:
                    tokens.append(make_token(src, SINGLE_COMM, start,
                                             CAT_COMMENT, 419, path + [419]))
                return
            elif utf8_comm(c):
                state = 418
            else:
                errors.append(E.bad_comment_char(src, src.pos, 418))
                bad = True
        elif state == 420:                          # multi-line comment text
            if c == ")":
                state = 421
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            elif utf8_comm(c) or c == "\n":
                state = 420
            else:
                errors.append(E.bad_comment_char(src, src.pos, 420))
                bad = True
        elif state == 421:                          # ')' read
            if c == "#":
                state = 422
            elif c == ")":
                state = 421
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            elif utf8_comm(c) or c == "\n":
                state = 420                         # the ) was comment text
            else:
                errors.append(E.bad_comment_char(src, src.pos, 421))
                bad = True
                state = 420
        elif state == 422:                          # ')#' read
            # 422 --delim_muco--> 423*.  Only whitespace may follow )# before
            # the newline / end of file (Comments Rules 2 and 6).
            p = src.pos
            while p < src.n and src.text[p] in whitespace:
                p += 1
            if p < src.n and src.text[p] != "\n":
                errors.append(E.after_multi_comment(src, p, src.slice(start)))
                return
            if not bad:
                tokens.append(make_token(src, MULTI_COMM, start, CAT_COMMENT,
                                         423, path + [423]))
            return
        src.advance()
        if path[-1] != state:       # loops (418 -> 418) are shown once
            path.append(state)
