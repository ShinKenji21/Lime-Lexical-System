# Lime-Lexical-System

Web-based lexical analyzer and tokenizer for the LIME compiler.

## Run locally on Windows

From this project directory, create a virtual environment, install the
dependencies, and start the Flask development server:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the server with `Ctrl+C`.

The web app uses `LimeLexer.py` for tokenization. Running that file directly
starts its desktop interface; run `app.py` to use the browser-based interface.
