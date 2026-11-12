/*
 * script.js - everything the LIME Lexical Analyzer page does in the browser.
 *
 * Keeps the line numbers next to the editor, sends the code to the server
 * (/analyze) when "Run Lexer" is clicked, draws the tokens in the table
 * (Line:Col, Lexeme, Token, Token Type) and the lexical errors in the
 * Error / Console Log.  "Clear" empties the editor and both outputs.  The "Show" checkboxes hide or show the newline,
 * whitespace, tab, comment and EOF tokens without asking the server again.
 */

// Tokens from the last run, so the Show checkboxes can redraw instantly.
let cachedTokens = [];

// Which checkbox controls which token names.
const TOGGLE_GROUPS = {
    newline: ['newline'],
    whitespace: ['space'],
    tab: ['tab'],
    comment: ['single_comm', 'multi_comm'],
    EOF: ['EOF'],
};

// --- Line numbers ---------------------------------------------------------------
function updateLineNumbers() {
    const textarea = document.getElementById('code');
    const lines = textarea.value.split('\n').length;
    const lineNumDiv = document.getElementById('line-numbers');
    lineNumDiv.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('<br>');
    document.getElementById('char-count').innerText = `${textarea.value.length} chars`;
    syncScroll();
}

function syncScroll() {
    const textarea = document.getElementById('code');
    document.getElementById('line-numbers').scrollTop = textarea.scrollTop;
}

// --- Token table ----------------------------------------------------------------
// Token names hidden right now (from the unticked Show checkboxes).
function hiddenTokenNames() {
    const hidden = new Set();
    document.querySelectorAll('.show-toggle').forEach(box => {
        if (!box.checked) TOGGLE_GROUPS[box.value].forEach(n => hidden.add(n));
    });
    return hidden;
}

// Makes invisible lexemes readable in the table.
// Invisible lexemes get a grey label instead, e.g. "(space)".
function invisibleLabel(t) {
    switch (t.token) {
        case 'space': return '(space)';
        case 'tab': return '(tab)';
        case 'newline': return '(newline)';
        case 'EOF': return '(EOF)';
        default: return null;
    }
}

function renderTokenTable() {
    const tbody = document.getElementById('token-table');
    const hidden = hiddenTokenNames();
    const shown = cachedTokens.filter(t => !hidden.has(t.token));
    tbody.innerHTML = '';

    document.getElementById('token-count').innerText = `${shown.length} Tokens`;

    if (shown.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-table-msg">No tokens generated.</td></tr>';
        return;
    }

    shown.forEach(t => {
        const tr = document.createElement('tr');
        const label = invisibleLabel(t);
        const lexemeCell = label
            ? `<span style="color: var(--text-muted)">${label}</span>`
            : `<code style="white-space: pre">${escapeHtml(t.lexeme)}</code>`;
        tr.innerHTML = `
            <td>${t.line}:${t.col}</td>
            <td>${lexemeCell}</td>
            <td><code>${escapeHtml(t.token)}</code></td>
            <td>${escapeHtml(t.token_type)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Run Lexer ------------------------------------------------------------------
async function runAnalysis() {
    const code = document.getElementById('code').value;

    const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
    });
    const data = await res.json();

    cachedTokens = data.tokens || [];
    renderTokenTable();

    const consoleLog = document.getElementById('console-log');
    const errStatus = document.getElementById('error-status');
    consoleLog.innerHTML = '';

    if (data.errors.length === 0) {
        errStatus.innerText = 'Status: OK (0 Errors)';
        errStatus.style.color = 'var(--primary-lime)';
        consoleLog.innerHTML = `<div class="log-success">✔ Tokenization succeeded — 0 lexical errors. Recognized ${cachedTokens.length} total tokens.</div>`;
        return;
    }

    errStatus.innerText = `Status: ${data.errors.length} Error(s) — ${cachedTokens.length} valid token(s)`;
    errStatus.style.color = 'var(--error-red)';

    data.errors.forEach((e, idx) => {
        const card = document.createElement('div');
        card.className = 'log-error-card';
        const state = (e.state !== null && e.state !== undefined) ? ` (stuck at state ${e.state})` : '';
        card.innerHTML = `
            <strong>[Error ${idx + 1}] ${escapeHtml(e.kind)} at ${e.line}:${e.col}${state}</strong><br>
            ${e.lexeme ? `<span>Invalid lexeme: <code>${escapeHtml(e.lexeme)}</code></span><br>` : ''}
            <span>Reason: ${escapeHtml(e.message)}</span><br>
            ${e.expected ? `<span style="color: var(--text-muted)">Expected: ${escapeHtml(e.expected)}</span>` : ''}
        `;
        consoleLog.appendChild(card);
    });
}

// --- Clear ------------------------------------------------------------------------
// Empties the editor and puts the token table and the log back to "ready".
function clearEditor() {
    cachedTokens = [];
    document.getElementById('code').value = '';
    updateLineNumbers();
    document.getElementById('token-table').innerHTML =
        '<tr><td colspan="4" class="empty-table-msg">Click \'▶ Run Lexer\' to display generated tokens.</td></tr>';
    document.getElementById('token-count').innerText = '0 Tokens';
    document.getElementById('console-log').innerHTML =
        '<span class="log-success">System initialized. Ready to tokenize LIME code.</span>';
    const errStatus = document.getElementById('error-status');
    errStatus.innerText = 'Status: Ready';
    errStatus.style.color = '';
    document.getElementById('code').focus();
}

// --- Helper -----------------------------------------------------------------------
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// --- Page start-up -----------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('code');
    textarea.addEventListener('scroll', syncScroll);
    textarea.addEventListener('input', updateLineNumbers);

    // Tab key types a tab character instead of moving focus out of the editor.
    textarea.addEventListener('keydown', e => {
        if (e.key !== 'Tab' || e.ctrlKey || e.altKey || e.metaKey) return;
        e.preventDefault();
        textarea.setRangeText('\t', textarea.selectionStart, textarea.selectionEnd, 'end');
        updateLineNumbers();
    });

    document.querySelectorAll('.show-toggle').forEach(box => {
        box.addEventListener('change', renderTokenTable);
    });

    updateLineNumbers();
});
