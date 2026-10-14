"""
app.py - the web server for the LIME Lexical Analyzer.

What it does, in general:
  * Shows the web page (templates/index.html) when you open the site.
  * Receives LIME code from the page, runs it through our lexer
    (LimeLexer.py), and sends back the list of valid tokens and the list of
    lexical errors as JSON so the page can draw the table and error log.
"""

# --- Imports -----------------------------------------------------------------
# Flask is the small web framework that serves the page and the /analyze API.
# Lexer is our own LIME lexer class from LimeLexer.py.
from flask import Flask, render_template, request, jsonify
from LimeLexer import Lexer

# Create the web application object.
app = Flask(__name__)

# --- Sample programs ------------------------------------------------------------
# SAMPLE_OK  : a program with no lexical errors (every lexeme reaches a final
#              state and is followed by a valid delimiter).
# SAMPLE_ERR : a program where each line triggers a different lexical error,
#              so we can demo how the error log looks.
SAMPLE_OK = '''#( LIME demo: constants, a function, loops and a struct )#
Same HELLO: Word = "Hello, " # a constant
Vary world: Word = "Lime \\"Grocer\\"\\n"
Vary count: Number = 0
Vary pi: Rational = 3.14
Vary temp: Rational = -4.5
Vary lowest: Number = -9223372036854775808
Vary flipped: Number = -count #unary negation
Vary open: Truth = True
Vary nums: Number[] = Basket[1, 2, 3]

Recipe Point {
    Number x
    Number y
}

Blend add(a: Number, b: Number) -> Number {
    Produce a + b
}'''

SAMPLE_ERR = '''Vary 4ever_lime: Number = 1
Vary big: Number = 123456789012345678901
Vary whole: Rational = 360.
Vary name: Word = 'Suisei'
Vary msg: Word = "path\\folder"
Blend(x) -> Bland {}
Vary q: Number = 10--5
#
Vary w: Word = "never closed
#( this comment is never closed'''

# --- Home page ------------------------------------------------------------------
# When someone opens http://127.0.0.1:5000/ we send them the editor page.
@app.route('/')
def home():
    return render_template('index.html', sample_ok=SAMPLE_OK, sample_err=SAMPLE_ERR)

# --- Lexical analysis API --------------------------------------------------------
# The page sends {"code": "..."} here when "Run Lexer" is clicked.
# We run the lexer, then turn its tokens and errors into plain dictionaries
# so they can be sent back as JSON.
@app.route('/analyze', methods=['POST'])
def analyze():
    # Read the code sent by the page (empty string if nothing was sent).
    data = request.json or {}
    source_code = data.get('code', '')
    
    # Run our LIME lexer over the whole program.
    lexer = Lexer(source_code)
    lexer.tokenize()
    
    # Package every VALID token (newline tokens included; the page can hide them).
    tokens_payload = []
    for tok in lexer.tokens:
        tokens_payload.append({
            'line': tok.line,
            'col': tok.col,
            'type': tok.type,
            'lexeme': tok.lexeme,
            'category': tok.category,
            'pattern': tok.pattern,
            'flagged': tok.flagged
        })

    # Package every lexical error (invalid lexemes go here, never in the token list).
    errors_payload = []
    for err in lexer.errors:
        errors_payload.append({
            'line': err.line,
            'col': err.col,
            'kind': err.kind,
            'message': err.message,
            'found': err.found,
            'expected': err.expected,
            'lexeme': err.lexeme
        })

    # Send both lists back to the page.
    return jsonify({
        'tokens': tokens_payload,
        'errors': errors_payload
    })

# --- Start the server -------------------------------------------------------------
# Only runs when you start this file directly with:  python app.py
if __name__ == '__main__':
    print("Starting LIME Lexical Analyzer Web App on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)