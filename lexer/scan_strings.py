"""
scan_strings.py - str_lit (TD E, states 386-389), one if / elif branch per
state.

0 --"--> 386,  386 --utf8_str--> 386,  386 --\\--> 389 --esc_char--> 386,
386 --"--> 387,  387 --val_delim--> 388*
"""

from .definitions import DELIM, utf8_str, esc_char, backslash
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
                state = 386
            else:
                return
        elif state == 386:                          # inside the Word
            if c == '"':
                state = 387
            elif c == backslash:
                state = 389
            elif utf8_str(c):
                state = 386
            elif c == "" or c == "\n":
                # no arrow on newline / EOF: the Word is never closed
                errors.append(E.unclosed_string(src, start, src.slice(start)))
                return
            else:
                # no arrow on this character: report what was read; scanning
                # goes back to state 0 at this character.
                errors.append(E.bad_string_char(src, start, src.pos, src.slice(start)))
                return
        elif state == 389:                          # '\' read
            if c != "" and c in esc_char:           # \n \t \" \\
                state = 386
            else:
                # no arrow on this character after the backslash: report what
                # was read; scanning goes back to state 0 at this character.
                errors.append(E.invalid_escape(src, start, src.pos, src.slice(start)))
                return
        elif state == 387:                          # closing quote read
            if c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 388, STR_LIT)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos,
                                                  "Word literal", src.slice(start),
                                                  "val_delim", 387))
                return
        src.advance()
        if path[-1] != state or state == 389:   # the 386 loop is shown once
            path.append(state)
