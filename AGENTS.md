# AGENTS.md

Project instructions for AI assistants working on this course repo.

## Goals
- Help develop and test Marimo notebooks for the photonics course.
- Keep edits minimal, clear, and consistent with existing patterns.

## Environment
- Use the local virtual environment at `.venv`.
- Prefer `./.venv/bin/python` and `./.venv/bin/pip` for any Python commands.
- Network access is allowed, but avoid adding new dependencies unless requested.

## Notebook development workflow
- For quick error checks, run:
  - `./.venv/bin/python -m py_compile <notebook.py>`
  - `./.venv/bin/python -c "import <module_path>"`
- Only start the Marimo server when explicitly requested.
- If a cell fails in VS Code, try to reproduce via import or targeted checks; report inferred root cause.

## Coding style
- Keep changes small and focused.
- Reuse patterns from existing notebooks (e.g., `_notebook_template.py`, `_style.py`).
- Add comments only when logic is not self-explanatory.
- Default to ASCII; do not introduce unicode unless already used in that file.

## What to report back
- Explain what changed and why, with file paths.
- If a check was run, summarize the outcome and any errors.
- Suggest next steps only when there are clear follow-ups.
