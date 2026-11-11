"""
app.py - the web server for the LIME Lexical Analyzer.

  * Shows the page (templates/index.html).
  * /analyze receives LIME code, runs it through the lexer package, and sends
    back every token (including newline, whitespace, tab, comment and EOF
    tokens, which the page can hide) and every lexical error as JSON.
"""

from flask import Flask, render_template, request, jsonify
from lexer import Lexer

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    lx = Lexer(data.get('code', ''))
    lx.tokenize()

    tokens_payload = [{
        'line': tok.line,
        'col': tok.col,
        'lexeme': tok.lexeme,
        'token': tok.type,
        'token_type': tok.category,
        'final_state': tok.final_state,
    } for tok in lx.tokens]

    errors_payload = [{
        'line': err.line,
        'col': err.col,
        'kind': err.kind,
        'message': err.message,
        'found': err.found,
        'expected': err.expected,
        'lexeme': err.lexeme,
        'state': err.state,
    } for err in lx.errors]

    return jsonify({'tokens': tokens_payload, 'errors': errors_payload})


if __name__ == '__main__':
    print("Starting LIME Lexical Analyzer Web App on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
