"""The LIME lexical analyzer, following the transition diagrams of the paper."""

from .lexer import Lexer, tokenize
from .tokens import Token
from .errors import LexicalError

__all__ = ["Lexer", "tokenize", "Token", "LexicalError"]
