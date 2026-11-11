"""
tokens.py - the Token class and the token names that are not reserved words
or reserved symbols (those use their own spelling as the token name).
"""

# Token names (the "Token" column of the output table)
ID = "id"
INT_LIT = "int_lit"
FLO_LIT = "flo_lit"
STR_LIT = "str_lit"
BOO_LIT = "boo_lit"
SINGLE_COMM = "single_comm"
MULTI_COMM = "multi_comm"
NEWLINE = "newline"
SPACE = "space"           # Regular Definitions: space, tab -> whitespace
TAB = "tab"
EOF = "EOF"

# Token types (the "Token Type" column)
CAT_IDENTIFIER = "Identifier"
CAT_LITERAL = "Literal"
CAT_COMMENT = "Comment"
CAT_NEWLINE = "Newline"
CAT_WHITESPACE = "Whitespace"   # token type of both space and tab
CAT_EOF = "End of File"


class Token:
    """One token.

    type      token name, e.g. Vary, id, int_lit, +=, newline
    lexeme    the exact text from the source
    line/col  where it starts (1-based)
    category  token type, e.g. Declaration, Identifier, Literal
    final_state / path  the transition-diagram states it went through
    """

    def __init__(self, ttype, lexeme, line, col, category,
                 final_state=None, path=None):
        self.type = ttype
        self.lexeme = lexeme
        self.line = line
        self.col = col
        self.category = category
        self.final_state = final_state
        self.path = path or []

    def __repr__(self):
        return "Token(%s, %r, %d:%d, %s)" % (self.type, self.lexeme,
                                             self.line, self.col, self.category)


def make_token(src, ttype, start, category, final_state=None, path=None,
               end=None):
    """Build a token for the text from `start` to the current position."""
    line, col = src.loc(start)
    return Token(ttype, src.slice(start, end), line, col, category,
                 final_state, path)
