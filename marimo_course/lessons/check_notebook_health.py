#!/usr/bin/env python3
"""
Quick sanity checks for marimo notebooks in this folder.

Usage:
  python3 Photonics-Bootcamp/marimo_course/lessons/check_notebook_health.py \
    Photonics-Bootcamp/marimo_course/lessons/w02_mzi_modelling.py
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _check_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if "app._unparsable_cell(" in text:
        warnings.append("Found `app._unparsable_cell(...)` (often indicates corrupted marimo export).")

    try:
        mod = ast.parse(text)
    except SyntaxError as e:
        errors.append(f"SyntaxError: {e}")
        mod = None

    if mod is not None:
        for node in ast.walk(mod):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple) and len(node.value.elts) == 1:
                errors.append(
                    f"Single-element tuple return at line {node.lineno} (likely `return (widget,)` bug)."
                )

    # Heuristic: if the notebook defines a "Plot status" line, ensure it is actually returned nearby.
    if "Plot status:" in text and "return mo.vstack([chart_out, status_line" not in text:
        warnings.append(
            "Notebook contains a Plot status line but does not appear to return it (plot cell may render blank)."
        )

    if errors:
        print(f"[FAIL] {path}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    else:
        print(f"[OK]   {path}")

    if warnings:
        print(f"[WARN] {path}", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    return 1 if errors else 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Provide one or more .py marimo notebooks.", file=sys.stderr)
        return 2

    rc = 0
    for arg in argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"[FAIL] Missing file: {p}", file=sys.stderr)
            rc = 1
            continue
        rc |= _check_file(p)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

