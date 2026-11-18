"""
reserved.py - the reserved words (RESERVED WORDS, pp. 13-17) and reserved
symbols (RESERVED SYMBOLS, pp. 18-21) of LIME with their token type.

The transition-diagram states for them are written out as if / elif
branches in scan_words.py and scan_symbols.py.
"""

# --- reserved words: word -> token type ----------------------------------------
RW_CATEGORY = {}
for _w in ("Vary", "Same", "Blend", "Recipe"):
    RW_CATEGORY[_w] = "Declaration"
RW_CATEGORY["Basket"] = "Array Constructor"
for _w in ("Number", "Rational", "Word", "Truth", "Bland"):
    RW_CATEGORY[_w] = "Data Type"
for _w in ("And", "Or", "Not"):
    RW_CATEGORY[_w] = "Logical Operator"
for _w in ("True", "False"):
    RW_CATEGORY[_w] = "Truth Literal"
for _w in ("Test", "Taste", "Stir", "Mix", "Pour", "Factor", "Harvest", "Try",
           "Unripe", "Reap", "Uproot", "Produce"):
    RW_CATEGORY[_w] = "Control Flow"
for _w in ("Absorb", "Squeeze", "ToNumber", "ToRational", "ToWord",
           "ToTruth", "Append", "Insert", "Remove", "Clear", "Length"):
    RW_CATEGORY[_w] = "Built-in Function"

RESERVED_WORDS = set(RW_CATEGORY)

# Token name: the word itself, except True / False which are boo_lit.
RW_TOKEN = {w: w for w in RESERVED_WORDS}
RW_TOKEN["True"] = "boo_lit"
RW_TOKEN["False"] = "boo_lit"

# First letters that have an arrow out of state 0 in TD A.
RW_START = set("ABCFHILMNOPRSTUVW")


# --- reserved symbols: symbol -> token type ---------------------------------------
SYM_CATEGORY = {}
for _s in ("+", "-", "*", "/", "%", "^"):
    SYM_CATEGORY[_s] = "Arithmetic Operator"
for _s in ("=", "+=", "-=", "*=", "/=", "%="):
    SYM_CATEGORY[_s] = "Assignment Operator"
for _s in (">", "<", ">=", "<=", "==", "!="):
    SYM_CATEGORY[_s] = "Comparison Operator"
for _s in ("++", "--"):
    SYM_CATEGORY[_s] = "Unary Operator"
SYM_CATEGORY["~"] = "Unary Negation"
SYM_CATEGORY.update({
    "(": "Open Parenthesis",
    ")": "Close Parenthesis",
    "[": "Open Bracket",
    "]": "Close Bracket",
    "{": "Open Brace",
    "}": "Close Brace",
    ":": "Colon",
    ";": "Semicolon",
    ".": "Period",
    ",": "Comma",
    "->": "Return Type Arrow",
})

# Characters that have an arrow out of state 0 in TD B.
SYMBOL_START = set("+-~*/%^=><!)([]{}:;.,")
