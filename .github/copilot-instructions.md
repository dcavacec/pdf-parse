# Guidance for AI coding agents working on PDF-Parse

This file captures the minimal, high-value knowledge an automated coding agent needs to be productive in this repository.

## Big picture
- The project provides a Python library and small apps to extract tabular data from PDFs.
- Core package: `pdf_parse/` (main classes: `parser.py`, `table.py`, `config.py`).
- Two user-facing surfaces:
  - Streamlit app: `app.py` (full UI and recommended entrypoint)
  - Simple HTML/Flask frontend: `simple_frontend.py` + `templates/index.html`
- Command-line interfaces:
  - Project CLI wrapper: `cli.py` (root) for quick runs
  - Packaged console entrypoint: `pdf-parse=pdf_parse.cli:main` (see `setup.py`)
- A separate helper/core file `pdf_table_extractor.py` contains additional extraction plumbing used by frontends/CLI examples.

## Key files to read before edits
- `pdf_parse/parser.py` — parsing flow, page loop, simple table-detection heuristics and error handling (continue-on-error).
- `pdf_parse/table.py` — Table representation and export helpers (CSV/JSON/string).
- `pdf_table_extractor.py` — higher-level extraction helpers used by `app.py` and root `cli.py`.
- `app.py` — Streamlit UI: how options map to extractor arguments and supported methods (`auto`, `pdfplumber`, `tabula`, `camelot`).
- `cli.py` and `pdf_parse/cli.py` — user-visible flags and output behaviors.
- `requirements.txt` / `setup.py` — runtime deps and dev extras (tests, linters).
- `tests/` — unit tests that act as a small spec (see `tests/test_parser.py`, `tests/test_table.py`).

## Common workflows & commands
- Development setup (recommended):
  - Create venv and install: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - Install editable package: `pip install -e .`
- Run Streamlit UI (recommended for manual testing):
  - `python -m streamlit run app.py` (default: http://localhost:8501)
- Run CLI examples / local CLI:
  - `python cli.py sample_tables.pdf --summary --verbose`
  - Packaged CLI: after `pip install -e .`, use `pdf-parse <file> ...`
- Run tests:
  - `python -m pytest` (or `python -m pytest tests/test_parser.py -q`)
  - Coverage: `python -m pytest --cov=pdf_parse`

## Project-specific conventions & patterns
- Extraction methods are enumerated in CLIs and the Streamlit UI: `auto`, `pdfplumber`, `tabula`, `camelot`. New backends must be wired into `pdf_table_extractor.py` and exposed where `method` is parsed.
- Error handling: parser code is tolerant — it prints warnings and continues processing pages. Preserve this behavior when modifying page loops so one bad page doesn't stop batch jobs.
- Table detection in `parser.py` uses a simple text-heuristic: look for tabs or multiple spaces and a `min_table_size` from `config.ParseConfig`. Tests assume this behavior.
- Data model: `Table` stores `data`, `columns`, exposes `to_csv`, `to_json`, `to_dict`, `to_string`. Use those helpers rather than duplicating export logic.
- I/O & defaults: If CLI frontends receive no explicit `--output`, they write to `<pdf_stem>_tables.xlsx` and a CSV folder `<pdf_stem>_tables/` — keep that default to avoid surprising consumers.

## Tests and quality gates
- Tests live in `tests/` and assert parser heuristics and Table exports. Run tests after changes; they are the fastest sanity check.
- Linting/formatting and dev extras are in `setup.py` (`pytest`, `flake8`, `black`). Keep changes small and run `pytest` locally in this order: tests -> lint -> optional coverage.

## Integration & external dependencies
- Key Python packages: `pypdf`, `pdfplumber`, `tabula-py`, `camelot-py`, `pandas`, `openpyxl`, `streamlit` (see `requirements.txt`).
- System packages: `ghostscript` (for `camelot`/`tabula`) and `python3-tk` (on some platforms). Document any extra apt/brew steps in PR descriptions when adding camelot-related code.

## When adding features or fixing bugs
- If touching parsing logic, update `tests/test_parser.py` with at least one regression test that demonstrates the previous failure and the new correct behavior.
- When adding a new extraction backend:
  1. Implement the extractor in `pdf_table_extractor.py` (add a clear function name and small docstring).
  2. Add mapping from `method` string to implementation where the CLI and `app.py` call the extractor.
  3. Add an example in `examples/` and a test exercising the new method (or a smoke test). 
- Keep CLI flags stable. If you must change CLI behavior, update `README.md`, `FRONTEND_README.md`, and `setup.py` if entrypoints change.

## Helpful examples (copy-paste safe)
- Streamlit: `python -m streamlit run app.py`
- CLI: `python cli.py sample_tables.pdf --pages 1,3 --method tabula --summary --verbose`
- Tests: `python -m pytest tests/test_table.py -q`

If anything in this file is unclear or you want the agent to follow a stricter policy (for example: always add tests, run linters, or avoid editing frontends), tell me what to change and I will iterate.
