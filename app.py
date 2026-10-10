from flask import Flask, render_template, request, jsonify
from LimeLexer import Lexer, SAMPLE_OK, SAMPLE_ERR

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', sample_ok=SAMPLE_OK, sample_err=SAMPLE_ERR)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    source_code = data.get('code', '')
    
    lexer = Lexer(source_code)
    lexer.tokenize()
    
    # Format tokens for the JSON response
    tokens_payload = []
    for tok in lexer.tokens:
        if tok.type == "newline":
            continue
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