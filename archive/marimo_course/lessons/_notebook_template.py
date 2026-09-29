from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Callable

import _style


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _escape_attr(value: str) -> str:
    return _escape_html(value)


def inject_css(mo) -> object:
    """Inject shared notebook CSS."""
    return _style.inject_css(mo)


def make_doc_helpers(mo):
    """Return callout helpers with the same signatures used in notebooks."""

    def _maybe_escape(value: str, *, allow_html: bool) -> str:
        if allow_html:
            return value
        return _escape_html(value)

    def _callout_kind(kind: str) -> str:
        # Map our course-level callout kinds to marimo's built-in kinds.
        mapping = {
            "info": "info",
            "warning": "warn",
            "warn": "warn",
            "success": "success",
            "danger": "danger",
            # Used for "Verify"/"Tool"/"Concept check" blocks; keep neutral styling.
            "exercise": "neutral",
            "neutral": "neutral",
        }
        return mapping.get(kind, "neutral")

    def _callout_title_md(*, tag: str, title: str) -> str:
        # Allow inline HTML (e.g., <code>n_eff</code>) in tag/title by not escaping.
        if tag and title:
            return f"**{tag}:** {title}"
        if tag:
            return f"**{tag}**"
        return f"**{title}**" if title else ""

    def doc_badges(badges: list[str], *, style: str | None = None) -> object:
        # Many notebooks pass HTML fragments inside badges (e.g., <strong>...</strong>),
        # so we intentionally do not escape badge strings.
        style_attr = f' style="{_escape_attr(style)}"' if style else ""
        inner = "".join(f'<span class="doc-badge">{b}</span>' for b in badges)
        return mo.md(f'<div class="doc-badges"{style_attr}>{inner}</div>')

    def doc_callout_list(
        kind: str,
        *,
        tag: str,
        title: str,
        items: list[str],
        ordered: bool = False,
    ) -> object:
        bullet_prefix = "1." if ordered else "-"
        list_md = "\n".join(f"{bullet_prefix} {item}" for item in items)
        title_md = _callout_title_md(tag=tag, title=title)
        body_md = _style.dedent(
            f"""
            {title_md}

            {list_md}
            """
        ).strip()
        return mo.callout(mo.md(body_md), kind=_callout_kind(kind))

    def doc_callout_html(
        kind: str,
        *,
        tag: str,
        title: str,
        html: str,
    ) -> object:
        # Despite the parameter name, we treat `html` as Markdown-capable content.
        # This avoids LaTeX-in-raw-HTML rendering issues while preserving existing callsites.
        title_md = _callout_title_md(tag=tag, title=title)
        body_md = _style.dedent(
            f"""
            {title_md}

            {html}
            """
        ).strip()
        return mo.callout(mo.md(body_md), kind=_callout_kind(kind))

    return doc_badges, doc_callout_html, doc_callout_list


def make_health_refresh_button(mo, *, label: str = "Re-run self-check"):
    """Button used to force a recompute of the self-check cell."""
    return mo.ui.button(
        value=0,
        on_click=lambda v: (v or 0) + 1,
        kind="neutral",
        label=label,
    )


def make_instructor_mode_toggle(
    mo, *, label: str = "Instructor mode", value: bool = False
):
    """A course-wide toggle for showing solutions/extra notes."""
    return mo.ui.checkbox(label=label, value=value)


def make_section_view(
    mo,
    *,
    options: list[str] | tuple[str, ...] = ("All", "Overview", "Theory", "Interactive", "Layout"),
    value: str = "All",
    label: str = "Notebook view",
    inline: bool = True,
):
    """
    A state-backed section selector so other UI elements can programmatically switch views.

    Returns: (section_view_widget, view_state, set_view)
    """
    view, set_view = mo.state(value)
    section_view = mo.ui.radio(
        options=list(options),
        value=view(),
        label=label,
        inline=inline,
        on_change=set_view,
    )
    return section_view, view, set_view


def make_section_tabs(
    mo,
    *,
    options: list[str] | tuple[str, ...] = ("All", "Overview", "Theory", "Interactive", "Layout"),
    value: str = "All",
    label: str = "Notebook sections",
    lazy: bool = True,
):
    """
    A state-backed section selector implemented as marimo tabs.

    Returns: (section_tabs, view_state, set_view)
    """
    view_state, set_view = mo.state(value)
    # Use a display:none placeholder so the tabs act like a pure control (no visible tab body).
    _hidden = "<div style='display:none'></div>"
    section_tabs = mo.ui.tabs(
        {option: mo.md(_hidden) for option in options},
        value=view_state(),
        on_change=set_view,
        lazy=lazy,
        label=label,
    )
    return section_tabs, view_state, set_view


def optional_import(module: str) -> tuple[Any | None, str]:
    """Import a module but return an error string instead of raising."""
    try:
        return __import__(module), ""
    except Exception as e:  # pragma: no cover
        return None, f"{type(e).__name__}: {e}"


def data_uri_for_bytes(data: bytes, *, mime: str, filename: str) -> str:
    """Create a download link href for bytes using a base64 data URI."""
    import base64

    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def badge_row(mo, badges: list[str], *, style: str | None = None) -> object:
    """
    Render a row of course-styled badges.

    Badge strings may contain HTML (e.g., <strong>...</strong>).
    """
    style_attr = f' style="{_escape_attr(style)}"' if style else ""
    inner = "".join(f'<span class="doc-badge">{b}</span>' for b in badges)
    return mo.md(f'<div class="doc-badges"{style_attr}>{inner}</div>')


def download_csv_button(
    mo,
    rows: list[dict],
    *,
    filename: str = "data.csv",
    label: str = "Download CSV",
    mimetype: str = "text/csv",
    preferred_fields: list[str] | None = None,
) -> object:
    """Create a `mo.download` button for a list of dict rows."""
    import csv
    import io

    if not rows:
        return mo.md("")

    preferred_fields = preferred_fields or []
    extra_fields = sorted(
        {k for row in rows for k in row.keys() if k not in set(preferred_fields)}
    )
    fieldnames = list(preferred_fields) + extra_fields

    csv_out = io.StringIO()
    writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, "") for k in fieldnames})

    return mo.download(
        csv_out.getvalue().encode("utf-8"),
        filename=filename,
        mimetype=mimetype,
        label=label,
    )


def make_fsr_tool_widgets(
    mo,
    *,
    auto_options: list[str] | None = None,
    auto_default: str = "Best available",
    auto_label: str = "Auto-measure from",
    lam1_label: str = "λ1 (nm)",
    lam2_label: str = "λ2 (nm)",
) -> tuple[object, object, object, object, object, object, object]:
    """
    Build state-backed widgets commonly used for "measure FSR" tools.

    Returns: (auto_source, lam1_nm, lam2_nm, lam1_state, lam2_state, set_lam1, set_lam2)
    """
    auto_options = auto_options or [
        "Best available",
        "Analytic",
        "Simphony",
        "Student expression",
    ]
    auto_source = mo.ui.dropdown(
        options=auto_options,
        value=auto_default,
        label=auto_label,
    )

    lam1_state, set_lam1 = mo.state("")
    lam2_state, set_lam2 = mo.state("")
    lam1_nm = mo.ui.text(value=lam1_state(), label=lam1_label, on_change=set_lam1)
    lam2_nm = mo.ui.text(value=lam2_state(), label=lam2_label, on_change=set_lam2)

    return auto_source, lam1_nm, lam2_nm, lam1_state, lam2_state, set_lam1, set_lam2


def safe_editing_panel(
    mo,
    doc_callout_html: Callable[..., object],
    health_refresh,
    *,
    restore_command: str,
    external_check_command: str,
) -> object:
    """Render a consistent 'safe editing' callout + the refresh button."""
    return mo.vstack(
        [
            doc_callout_html(
                "info",
                tag="Maintenance",
                title="Safe editing + fast recovery",
                html=(
                    "<ul>"
                    "<li>After edits, click <strong>Re-run self-check</strong> (below). If it warns about "
                    "<code>app._unparsable_cell(...)</code>, the file is corrupted.</li>"
                    "<li>If the notebook breaks (missing sections, “return outside function”), recover with:</li>"
                    "</ul>"
                    f"<pre><code>{_escape_html(restore_command)}</code></pre>"
                    "<p>Then restart marimo.</p>"
                    "<p>If you want an external check, run:</p>"
                    f"<pre><code>{_escape_html(external_check_command)}</code></pre>"
                ),
            ),
            health_refresh,
        ]
    )


def notebook_self_check_view(
    *,
    doc_badges: Callable[..., object],
    doc_callout_html: Callable[..., object],
    notebook_path: str | Path,
    refresh_token: int | None = None,
) -> object:
    """Return a marimo view (badge or warning callout) for notebook health."""

    notebook_path = Path(notebook_path)
    problems: list[str] = []

    if refresh_token is not None:
        _ = refresh_token

    try:
        text = notebook_path.read_text(encoding="utf-8")
    except Exception as e:  # pragma: no cover
        problems.append(f"Could not read notebook source: `{type(e).__name__}: {e}`")
        text = ""

    def _has_unparsable_cell_line(source: str) -> bool:
        for line in source.splitlines():
            if line.lstrip().startswith("app._unparsable_cell("):
                return True
        return False

    if _has_unparsable_cell_line(text):
        problems.append(
            "Found `app._unparsable_cell(...)` (usually means the file was corrupted by an export)."
        )

    try:
        mod = ast.parse(text) if text else None
    except SyntaxError as e:
        problems.append(f"Notebook has a SyntaxError: `{e}`")
        mod = None

    def _is_app_cell(decorator: ast.AST) -> bool:
        d = decorator
        if isinstance(d, ast.Call):
            d = d.func
        return (
            isinstance(d, ast.Attribute)
            and isinstance(d.value, ast.Name)
            and d.value.id == "app"
            and d.attr == "cell"
        )

    if mod is not None:
        exported: dict[str, list[int]] = {}

        for node in mod.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if not any(_is_app_cell(d) for d in node.decorator_list):
                continue

            return_nodes = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
            if not return_nodes:
                continue

            ret = return_nodes[-1].value
            if ret is None:
                continue

            if isinstance(ret, ast.Name):
                returned_names = [ret.id]
            elif isinstance(ret, ast.Tuple):
                returned_names = [e.id for e in ret.elts if isinstance(e, ast.Name)]
            else:
                returned_names = []

            for name in returned_names:
                exported.setdefault(name, []).append(node.lineno)

        duplicates = {k: v for k, v in exported.items() if len(v) > 1}
        if duplicates:
            sensitive = ["blocks", "base64", "csv", "io", "Path"]
            sensitive_dupes = {k: v for k, v in duplicates.items() if k in sensitive}
            to_report = sensitive_dupes or duplicates
            items = "".join(
                f"<li><code>{_escape_html(name)}</code> exported by multiple cells (lines {', '.join(map(str, lines))})</li>"
                for name, lines in sorted(to_report.items())
            )
            problems.append(f"Duplicate exported variables detected:<ul>{items}</ul>")

    if problems:
        details = "".join(
            f'<div style="margin: 0.25rem 0;">{p}</div>' for p in problems
        )
        return doc_callout_html(
            "warning",
            tag="Self-check",
            title="Notebook health warning",
            html=(
                "<p>This notebook may behave unexpectedly (or be partially corrupted).</p>"
                f"{details}"
                "<p style=\"margin-top: 0.6rem;\">"
                "If you just edited this file and things broke, recover with your restore command and restart marimo."
                "</p>"
            ),
        )

    return doc_badges(
        [
            "Self-check: <strong>OK</strong>",
            f"<code>{_escape_html(notebook_path.name)}</code>",
        ]
    )
