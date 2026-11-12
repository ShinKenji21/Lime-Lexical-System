"""
scan_comments.py - single_comm and multi_comm (TD C, states 409-415), one
if / elif branch per state.

0 --#--> 409
  409 --delim_sico--> 411*                     empty comment: # then newline/EOF
  409 --utf8_no_oppa--> 410 --utf8_comm--> 410 --delim_sico--> 411*
  409 --(--> 412 --utf8_comm/newline--> 412 --)--> 413 --#--> 414
       414 --delim_muco--> 415*

At 413 a ) that is not followed by # is comment text (Comments Rule 7), so
413 goes back to 412 (or stays at 413 on another ')').
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
                state = 409
            else:
                return
        elif state == 409:                          # '#'
            if c in DELIM["delim_sico"]:            # empty comment
                tokens.append(make_token(src, SINGLE_COMM, start, CAT_COMMENT,
                                         411, path + [411]))
                return
            elif c == "(":
                state = 412
            elif utf8_no_oppa(c):
                state = 410
            else:
                errors.append(E.bad_comment_char(src, src.pos, 409))
                bad = True
                state = 410
        elif state == 410:                          # single-line comment text
            if c in DELIM["delim_sico"]:
                if not bad:
                    tokens.append(make_token(src, SINGLE_COMM, start,
                                             CAT_COMMENT, 411, path + [411]))
                return
            elif utf8_comm(c):
                state = 410
            else:
                errors.append(E.bad_comment_char(src, src.pos, 410))
                bad = True
        elif state == 412:                          # multi-line comment text
            if c == ")":
                state = 413
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            elif utf8_comm(c) or c == "\n":
                state = 412
            else:
                errors.append(E.bad_comment_char(src, src.pos, 412))
                bad = True
        elif state == 413:                          # ')' read
            if c == "#":
                state = 414
            elif c == ")":
                state = 413
            elif c == "":
                errors.append(E.unclosed_comment(src, start, src.slice(start)))
                return
            elif utf8_comm(c) or c == "\n":
                state = 412                         # the ) was comment text
            else:
                errors.append(E.bad_comment_char(src, src.pos, 413))
                bad = True
                state = 412
        elif state == 414:                          # ')#' read
            # 414 --delim_muco--> 415*.  Only whitespace may follow )# before
            # the newline / end of file (Comments Rules 2 and 6).
            p = src.pos
            while p < src.n and src.text[p] in whitespace:
                p += 1
            if p < src.n and src.text[p] != "\n":
                errors.append(E.after_multi_comment(src, p, src.slice(start)))
                return
            if not bad:
                tokens.append(make_token(src, MULTI_COMM, start, CAT_COMMENT,
                                         415, path + [415]))
            return
        src.advance()
        if path[-1] != state:       # loops (410 -> 410) are shown once
            path.append(state)
