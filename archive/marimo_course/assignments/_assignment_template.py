from __future__ import annotations

from pathlib import Path
import sys


def _ensure_lessons_on_path() -> Path:
    """
    Allow assignment notebooks to reuse the shared lesson UI/template code.

    Lessons live in `../lessons/` and are imported as plain modules (script-style).
    """
    lessons_dir = Path(__file__).resolve().parents[1] / "lessons"
    sys.path.insert(0, str(lessons_dir))
    return lessons_dir


def load_lesson_template():
    """
    Import and return the shared helpers used by lesson notebooks.

    Returns:
      inject_css, make_doc_helpers, make_health_refresh_button, header
    """
    _ensure_lessons_on_path()

    from _notebook_template import inject_css, make_doc_helpers, make_health_refresh_button
    from _style import header

    return inject_css, make_doc_helpers, make_health_refresh_button, header

