"""
emit.py - small helpers the scanners call when they reach a final state
(the double circle of a transition diagram).  Kept apart from the scanners so
the scan_*.py files are only the if / elif state chains.
"""

from .reserved import RW_TOKEN, RW_CATEGORY, SYM_CATEGORY
from .tokens import make_token, ID, CAT_IDENTIFIER, CAT_LITERAL
from .definitions import id_chars
from . import errors as E


def accept_word(src, tokens, start, path, final, word):
    """Reserved word reached its final state, e.g. 199 --delim_decl--> 200*."""
    token = RW_TOKEN[word]
    category = CAT_LITERAL if token == "boo_lit" else RW_CATEGORY[word]
    tokens.append(make_token(src, token, start, category, final, path + [final]))


def word_delimiter_error(src, errors, start, state, word, delim):
    """Reserved word fully spelled but followed by a character that is neither
    its delimiter nor a letter/digit/_ (so it is not a longer identifier)."""
    errors.append(E.invalid_delimiter(src, start, src.pos, "Reserved word",
                                      word, delim, state))


def accept_id(src, tokens, start, path, final):
    tokens.append(make_token(src, ID, start, CAT_IDENTIFIER, final,
                             path + [final]))


def accept_literal(src, tokens, start, path, final, token):
    tokens.append(make_token(src, token, start, CAT_LITERAL, final,
                             path + [final]))


def accept_symbol(src, tokens, start, path, final, sym):
    tokens.append(make_token(src, sym, start, SYM_CATEGORY[sym], final,
                             path + [final]))


def absorb(src, chars):
    """Error recovery: swallow the rest of a run of characters so it is
    reported as one invalid lexeme (e.g. all of 4ever_lime)."""
    while src.peek() != "" and src.peek() in chars:
        src.advance()


def number_delimiter_error(src, errors, start, state, what, delim):
    err = E.invalid_delimiter(src, start, src.pos, what, src.slice(start),
                              delim, state)
    if src.peek() in id_chars:
        absorb(src, id_chars)
        err.lexeme = src.slice(start)
    errors.append(err)
