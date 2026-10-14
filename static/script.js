/*
 * script.js - everything the LIME Lexical Analyzer page does in the browser.
 *
 * In general: it keeps the line numbers next to the editor, loads/saves/imports
 * code, sends the code to the server (/analyze) when "Run Lexer" is clicked,
 * and then draws the valid tokens in the table (right side) and the lexical
 * errors in the Error / Console Log (bottom).
 */

// --- Sample programs ------------------------------------------------------------
// sampleOk  : a program with zero lexical errors.
// sampleErr : each line shows a different kind of lexical error.
// (These are the same programs as SAMPLE_OK / SAMPLE_ERR in app.py.)
const sampleOk = `#( LIME demo: constants, a function, loops and a struct )#
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
}`;

const sampleErr = `Vary 4ever_lime: Number = 1
Vary big: Number = 123456789012345678901
Vary whole: Rational = 360.
Vary name: Word = 'Suisei'
Vary msg: Word = "path\\folder"
Blend(x) -> Bland {}
Vary q: Number = 10--5
#
Vary w: Word = "never closed
#( this comment is never closed`;

// --- Token cache ----------------------------------------------------------------
// Keeps the tokens from the last run so the "Show newline tokens" checkbox can
// redraw the table instantly without asking the server again.
let cachedTokens = [];

// --- Line numbers ---------------------------------------------------------------
// updateLineNumbers: counts the lines in the editor, writes 1, 2, 3 ... in the
// gutter on the left, and updates the character counter in the header.
function updateLineNumbers() {
    const textarea = document.getElementById('code');
    const lines = textarea.value.split('\n').length;
    const lineNumDiv = document.getElementById('line-numbers');
    lineNumDiv.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('<br>');
    document.getElementById('char-count').innerText = `${textarea.value.length} chars`;
    syncScroll();
}

// syncScroll: keeps the line-number gutter scrolled to the same spot as the editor.
function syncScroll() {
    const textarea = document.getElementById('code');
    const lineNumDiv = document.getElementById('line-numbers');
    lineNumDiv.scrollTop = textarea.scrollTop;
}

// --- Reset ----------------------------------------------------------------------
// Clears the token table and the error log back to their "ready" state.
// Used whenever the code in the editor is replaced.
function resetOutputViews() {
    cachedTokens = [];
    document.getElementById('token-table').innerHTML = '<tr><td colspan="4" class="empty-table-msg">Click \'▶ Run Lexer\' to display generated tokens.</td></tr>';
    document.getElementById('token-count').innerText = '0 Tokens';
    document.getElementById('console-log').innerHTML = '<span>Ready to analyze LIME code.</span>';
    const errStatus = document.getElementById('error-status');
    errStatus.innerText = 'Status: Ready';
    errStatus.style.color = 'var(--text-muted)';
}

// --- Sample / Clear buttons ------------------------------------------------------
// loadSample: puts the valid ('ok') or error ('err') sample into the editor.
function loadSample(type) {
    document.getElementById('code').value = type === 'ok' ? sampleOk : sampleErr;
    updateLineNumbers();
    resetOutputViews();
}

// clearEditor: empties the editor and the outputs.
function clearEditor() {
    document.getElementById('code').value = '';
    updateLineNumbers();
    resetOutputViews();
}

// --- Import File ----------------------------------------------------------------
// triggerImport opens the hidden file picker; handleFileImport reads the chosen
// .txt/.lime file and places its text in the editor.
function triggerImport() {
    document.getElementById('file-input').click();
}

function handleFileImport(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('code').value = e.target.result;
        updateLineNumbers();
        resetOutputViews();
    };
    reader.readAsText(file);
    event.target.value = '';
}

// --- Save File ------------------------------------------------------------------
// Downloads the current editor text as program.txt.
function saveToFile() {
    const code = document.getElementById('code').value;
    const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'program.txt';
    link.click();
    URL.revokeObjectURL(link.href);
}

// --- Token table ----------------------------------------------------------------
// Draws the cached tokens in the right-hand table (Line:Col, Token Type, Lexeme,
// Category). Newline tokens are hidden unless the checkbox is ticked.
function renderTokenTable() {
    const tbody = document.getElementById('token-table');
    const showNewlines = document.getElementById('show-newlines').checked;
    tbody.innerHTML = '';

    let displayTokens = cachedTokens;
    if (!showNewlines) {
        displayTokens = displayTokens.filter(t => t.type !== 'newline');
    }

    document.getElementById('token-count').innerText = `${displayTokens.length} Tokens`;

    if (displayTokens.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-table-msg">No tokens generated.</td></tr>';
        return;
    }

    displayTokens.forEach(t => {
        // Only valid tokens reach the table; invalid ones are reported in the
        // Error / Console Log instead.
        const tr = document.createElement('tr');

        // Render '\n' visually as explicit text in the table
        const displayLexeme = t.type === 'newline' ? '\\n' : t.lexeme;

        tr.innerHTML = `
            <td>${t.line}:${t.col}</td>
            <td><code>${escapeHtml(t.type)}</code></td>
            <td><code>${escapeHtml(displayLexeme)}</code></td>
            <td>${escapeHtml(t.category)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Run Lexer ------------------------------------------------------------------
// Sends the editor text to the server, stores the returned tokens, draws the
// table, then fills the Error / Console Log: a green success line if there are
// no errors, otherwise one red card per error showing the invalid lexeme,
// the reason, and what was expected.
async function runAnalysis() {
    const code = document.getElementById('code').value;

    const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
    });

    const data = await res.json();
    
    // Store full token array in cache and render
    cachedTokens = data.tokens || [];
    renderTokenTable();

    // Render Error / Console Log
    const consoleLog = document.getElementById('console-log');
    const errStatus = document.getElementById('error-status');
    consoleLog.innerHTML = '';

    if (data.errors.length === 0) {
        errStatus.innerText = 'Status: OK (0 Errors)';
        errStatus.style.color = 'var(--primary-lime)';
        consoleLog.innerHTML = `<div class="log-success">✔ Tokenization succeeded — 0 lexical errors. Recognized ${cachedTokens.length} total tokens.</div>`;
    } else {
        errStatus.innerText = `Status: ${data.errors.length} Error(s) — ${cachedTokens.length} valid token(s)`;
        errStatus.style.color = 'var(--error-red)';
        
        data.errors.forEach((e, idx) => {
            const card = document.createElement('div');
            card.className = 'log-error-card';
            card.innerHTML = `
                <strong>[Error ${idx + 1}] ${escapeHtml(e.kind)} at ${e.line}:${e.col}</strong><br>
                ${e.lexeme ? `<span>Invalid lexeme: <code>${escapeHtml(e.lexeme)}</code></span><br>` : ''}
                <span>Reason: ${escapeHtml(e.message)}</span><br>
                ${e.expected ? `<span style="color: var(--text-muted)">Expected: ${escapeHtml(e.expected)}</span>` : ''}
            `;
            consoleLog.appendChild(card);
        });
    }
}

// --- Helper -----------------------------------------------------------------------
// escapeHtml: makes text safe to put inside the page, so code like <b> or "
// is shown as text instead of being treated as HTML.
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// --- Page start-up -----------------------------------------------------------------
// When the page finishes loading: hook up scrolling/typing in the editor to the
// line numbers, make the newline checkbox redraw the table, and draw the first
// line numbers.
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('code');
    const newlineCheckbox = document.getElementById('show-newlines');

    // Sync line counter and scroll position
    textarea.addEventListener('scroll', syncScroll);
    textarea.addEventListener('input', updateLineNumbers);

    // Live update token table when checkbox toggling changes
    if (newlineCheckbox) {
        newlineCheckbox.addEventListener('change', renderTokenTable);
    }

    updateLineNumbers();
});