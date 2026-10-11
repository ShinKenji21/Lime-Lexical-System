from flask import Flask, render_template, request, jsonify
from LimeLexer import Lexer

app = Flask(__name__)

# Standard sample programs defined directly in app.py
SAMPLE_OK = '''#( LIME demo: constants, a function, loops and a struct )#
Same HELLO: Word = "Hello, " # a constant
Vary world: Word = "Lime \\"Grocer\\"\\n"
Vary count: Number = 0
Vary pi: Rational = 3.14
Vary temp: Rational = -4.5
Vary lowest: Number = -2147483648
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
Vary big: Number = 2147483648
Vary whole: Rational = 360.
Vary name: Word = 'Suisei'
Vary msg: Word = "path\\folder"
Blend(x) -> Bland {}
Vary q: Number = 10--5
Vary w: Word = "never closed
#( this comment is never closed'''

@app.route('/')
def home():
    return render_template('index.html', sample_ok=SAMPLE_OK, sample_err=SAMPLE_ERR)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    source_code = data.get('code', '')
    
    lexer = Lexer(source_code)
    lexer.tokenize()
    
    # Format tokens for the JSON response (including newline tokens)
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

    # Format errors for the JSON response
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

    return jsonify({
        'tokens': tokens_payload,
        'errors': errors_payload
    })

if __name__ == '__main__':
    print("Starting LIME Lexical Analyzer Web App on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)