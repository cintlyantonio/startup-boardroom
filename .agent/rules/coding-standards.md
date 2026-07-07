# Coding Standards

- PEP 8 compliance.
- Type hints on all functions.
- Docstrings on public functions.
- All Gemini API calls must be async and wrapped in `try/except` with retry logic.
- No `print()` statements in `src/` — use the `logging` module.
