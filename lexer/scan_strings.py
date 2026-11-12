"""
scan_strings.py - str_lit (TD C, states 406-408), one if / elif branch per
state.

0 --"--> 406,  406 --utf8_str / escapeseq--> 406,  406 --"--> 407,
407 --delim_str--> 408*
"""

from .definitions import DELIM, utf8_str, escapeseq, backslash
from .emit import accept_literal
from .tokens import STR_LIT
from . import errors as E


def scan_string(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:                              # start
            if c == '"':
                state = 406
            else:
                return
        elif state == 406:                          # inside the Word
            if c == '"':
                state = 407
            elif c == backslash:
                nxt = src.peek(1)
                if nxt != "" and nxt in escapeseq:
                    src.advance()                   # 406 --escapeseq--> 406
                    src.advance()
                    continue
                # Not \n \t \\ \" : no arrow on the character after the
                # backslash.  Report what was read; scanning goes back to
                # state 0 at that character.
                src.advance()
                errors.append(E.invalid_escape(src, start, src.pos, src.slice(start)))
                return
            elif c == "" or c == "\n":
                errors.append(E.unclosed_string(src, start, src.slice(start)))
                return
            elif utf8_str(c):
                src.advance()                       # 406 --utf8_str--> 406
                continue
            else:
                # no arrow on this character: report what was read; scanning
                # goes back to state 0 at this character.
                errors.append(E.bad_string_char(src, start, src.pos, src.slice(start)))
                return
        elif state == 407:                          # closing quote read
            if c in DELIM["delim_str"]:
                accept_literal(src, tokens, start, path, 408, STR_LIT)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos,
                                                  "Word literal", src.slice(start),
                                                  "delim_str", 407))
                return
        src.advance()
        path.append(state)
