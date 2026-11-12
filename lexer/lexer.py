"""
lexer.py - the main loop (state 0 of every diagram).

Looks at one character and sends it to the scanner whose diagram starts with
that arrow.  Newlines, runs of spaces, runs of tabs, comments and EOF are
also emitted as tokens so the page can show or hide them.

Errors are collected (not raised) so a single run reports all of them;
tokenize(raise_on_error=True) raises the first one afterwards.
"""

from .source import Source
from .definitions import numbers, letters
from .reserved import RW_START, SYMBOL_START
from .tokens import (make_token, NEWLINE, SPACE, TAB, EOF,
                     CAT_NEWLINE, CAT_WHITESPACE, CAT_EOF)
from . import errors as E
from .scan_words import scan_word, scan_identifier, scan_underscore
from .scan_numbers import scan_number
from .scan_strings import scan_string
from .scan_comments import scan_comment
from .scan_symbols import scan_symbol


class Lexer:
    def __init__(self, text):
        self.src = Source(text)
        self.tokens = []
        self.errors = []

    def tokenize(self, raise_on_error=False):
        src, tokens, errors = self.src, self.tokens, self.errors
        while True:
            c = src.peek()
            start = src.pos

            if c == "":                                   # end of file
                tokens.append(make_token(src, EOF, start, CAT_EOF))
                break

            if c == "\n":                                 # newline
                src.advance()
                tokens.append(make_token(src, NEWLINE, start, CAT_NEWLINE))
            elif c == " ":                                # one space = one token
                src.advance()
                tokens.append(make_token(src, SPACE, start, CAT_WHITESPACE))
            elif c == "\t":                               # one tab = one token
                src.advance()
                tokens.append(make_token(src, TAB, start, CAT_WHITESPACE))
            elif c == "#":                                # 0 --#--> 409
                scan_comment(src, tokens, errors)
            elif c == '"':                                # 0 --"--> 406
                scan_string(src, tokens, errors)
            elif c in numbers:                            # 0 --zero/nonzero--> 331/333
                scan_number(src, tokens, errors)
            elif c == "~" and src.peek(1) in numbers and src.peek(1) != "":
                scan_number(src, tokens, errors)          # 0 --~--> 220 --digit--> 331/333
            elif c in letters:
                if c in RW_START:                         # 0 --A--> 1, 0 --B--> 17, ...
                    scan_word(src, tokens, errors)
                else:                                     # 0 --letters--> 271
                    scan_identifier(src, tokens, errors)
            elif c == "_":
                scan_underscore(src, tokens, errors)
            elif c in SYMBOL_START:                       # 0 --+--> 206, ...
                scan_symbol(src, tokens, errors)
            else:
                errors.append(E.illegal_character(src, start))
                src.advance()

        if raise_on_error and errors:
            first = errors[0]
            first.errors = errors
            raise first
        return tokens


def tokenize(text, raise_on_error=True):
    """Return the list of tokens for `text`.  Raises the first LexicalError
    (with .errors holding all of them) unless raise_on_error is False."""
    return Lexer(text).tokenize(raise_on_error=raise_on_error)
