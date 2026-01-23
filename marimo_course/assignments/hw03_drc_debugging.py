#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.18.0",
#   "pyzmq",
#   "gdsfactory",
#   "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from _assignment_template import _ensure_lessons_on_path, load_lesson_template

    _ensure_lessons_on_path()

    inject_css, make_doc_helpers, make_health_refresh_button, header = load_lesson_template()
    inject_css(mo)

    doc_badges, doc_callout_html, doc_callout_list = make_doc_helpers(mo)
    return doc_callout_list, doc_callout_html, header, make_health_refresh_button, mo


@app.cell(hide_code=True)
def _(header, mo):
    header(
        mo,
        title="HW03 — DRC debugging + verification workflow",
        subtitle=(
            "Fix DRC errors in your HW02 submission GDS, then practice identifying and fixing "
            "common silicon-photonics layout errors using three intentionally-broken circuits."
        ),
        badges=["Week 3", "Homework", "Verification", "DRC debugging"],
        toc=[
            ("Overview", "overview"),
            ("Part A — Fix HW02 DRC", "part-a"),
            ("Part B — 3 broken circuits", "part-b"),
            ("Submission", "submit"),
        ],
        build="2026-01-23",
    )
    return


@app.cell(hide_code=True)
def _(doc_callout_list, mo):
    overview_md = mo.md(
        r"""
<a id="overview"></a>
## Overview

This homework is about the verification loop:

1. Run DRC on a GDS file.
2. Read the error report (.lyrdb).
3. Locate the geometry that caused the error.
4. Fix the layout.
5. Re-run DRC until it is clean.

This assignment focuses on **silicon photonics layouts** (Si + PinRec + DevRec + Floorplan).
"""
    )

    doc_callout_list(
        "info",
        tag="What to submit",
        title="Submission checklist",
        ordered=True,
        items=[
            "A DRC-cleaned version of your HW02 submission GDS (same filename as your HW02 submission).",
            "The corresponding DRC report (.lyrdb) after your fixes.",
            "For each of the 3 practice circuits: (a) the broken GDS + .lyrdb, and (b) the fixed GDS + .lyrdb.",
            "A short note (3–6 sentences): what the error was, how you found it, and what change fixed it.",
        ],
    )
    return (overview_md,)


@app.cell(hide_code=True)
def _(overview_md):
    overview_md
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-a"></a>
            ## Part A — Fix all DRC errors in your HW02 submission GDS

            1. Point the path below to **your HW02 submission GDS** in `openEBL-2026-02/submissions/`.
            2. Run DRC and inspect the reported categories/counts.
            3. Fix the layout (in your HW02 notebook / layout generation code).
            4. Re-export the GDS and re-run DRC until the report is clean (**0 items**).
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    username = mo.ui.text(
        value="your_username",
        label="Username (used only for filenames below)",
        full_width=False,
    )
    hw02_gds_path = mo.ui.text(
        value="openEBL-2026-02/submissions/EBeam_your_username.gds",
        label="HW02 submission GDS path",
        full_width=True,
    )
    run_hw02_drc = mo.ui.button(
        value=0,
        label="Run DRC on HW02 submission",
        kind="success",
        on_click=lambda v: (v or 0) + 1,
    )
    mo.vstack([username, hw02_gds_path, run_hw02_drc])
    return hw02_gds_path, run_hw02_drc, username


@app.cell
def _(doc_callout_html, hw02_gds_path, mo, run_hw02_drc):
    import subprocess as _subprocess
    from pathlib import Path as _Path
    import xml.etree.ElementTree as _ET

    _view = mo.md("Click **Run DRC on HW02 submission** to generate a `.lyrdb` report.")

    if run_hw02_drc.value > 0:
        _out = []

        _gds_path = _Path(hw02_gds_path.value).expanduser()
        if not _gds_path.exists():
            _out.append(
                mo.callout(mo.md(f"**GDS not found:** `{_gds_path}`"), kind="danger")
            )
            _view = mo.vstack(_out)
        else:
            _drc_script = _Path("marimo_course/scripts/run_klayout_drc.sh").resolve()
            _lyrdb_path = _gds_path.with_suffix(".lyrdb")

            _result = _subprocess.run(
                ["bash", str(_drc_script), str(_gds_path), str(_lyrdb_path)],
                capture_output=True,
                text=True,
                timeout=240,
            )
            if _result.returncode != 0:
                _out.append(
                    mo.callout(
                        mo.md(f"**DRC failed:**\n```\n{_result.stderr.strip()}\n```"),
                        kind="danger",
                    )
                )
                _view = mo.vstack(_out)
            else:
                _counts = {}
                if _lyrdb_path.exists():
                    root = _ET.parse(_lyrdb_path).getroot()
                    for item in root.findall(".//item"):
                        cat = item.find("category")
                        if cat is None or cat.text is None:
                            continue
                        name = cat.text.strip("'")
                        _counts[name] = _counts.get(name, 0) + 1

                _total = sum(_counts.values())
                _kind = "success" if _total == 0 else "warn"

                _rows = "".join(
                    f"<tr><td style='padding:6px;border:1px solid #ddd'>{k}</td>"
                    f"<td style='padding:6px;border:1px solid #ddd;text-align:center'>{v}</td></tr>"
                    for k, v in sorted(_counts.items())
                )
                _table = f"""
<table style="width: 100%; border-collapse: collapse; margin-top: 8px;">
  <thead>
    <tr style="background:#f0f0f0">
      <th style="padding:6px;border:1px solid #ddd;text-align:left">Category</th>
      <th style="padding:6px;border:1px solid #ddd;text-align:center">Count</th>
    </tr>
  </thead>
  <tbody>{_rows or "<tr><td colspan='2' style='padding:6px;border:1px solid #ddd'>No items</td></tr>"}</tbody>
</table>
"""
                _out.append(
                    mo.callout(
                        mo.md(
                            f"**DRC completed.** Total items: **{_total}**\n\n"
                            f"- GDS: `{_gds_path}`\n"
                            f"- Report: `{_lyrdb_path}`"
                        ),
                        kind=_kind,
                    )
                )
                _out.append(
                    doc_callout_html(
                        "info", tag="Counts", title="DRC report summary", html=_table
                    )
                )
                _view = mo.vstack(_out)

    _view
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-b"></a>
            ## Part B — Build 3 photonic circuits with errors, then fix them

            Create three small circuits, each with a different **silicon-photonics** verification issue:

            1. **Si width violation** (too narrow)
            2. **Si space violation** (too close)
            3. **PinRec connectivity warning** (PinRec not inside Si)

            For each circuit:
            1. Generate the **broken** GDS and run DRC (confirm it reports an error).
            2. Fix the layout by editing the parameters/cell below.
            3. Regenerate the **fixed** GDS and re-run DRC (confirm **0 items**).

            All generated files go to `openEBL-2026-02/hw03_debug/` (not the submissions folder).
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    from pathlib import Path as _Path

    artifacts_dir = mo.ui.text(
        value="openEBL-2026-02/hw03_debug",
        label="HW03 artifacts folder",
        full_width=True,
    )
    return artifacts_dir


@app.cell
def _(artifacts_dir, mo, username):
    from pathlib import Path as _Path

    base = _Path(artifacts_dir.value).expanduser()
    base.mkdir(parents=True, exist_ok=True)

    mo.callout(mo.md(f"Artifacts folder: `{base}` (username: `{username.value}`)"), kind="info")
    return


@app.cell
def _(artifacts_dir, mo, username):
    import subprocess as _subprocess
    from pathlib import Path as _Path
    import xml.etree.ElementTree as _ET

    def run_drc(gds_path: _Path) -> tuple[_Path, int, dict[str, int], str]:
        _drc_script = _Path("marimo_course/scripts/run_klayout_drc.sh").resolve()
        _lyrdb_path = gds_path.with_suffix(".lyrdb")
        _result = _subprocess.run(
            ["bash", str(_drc_script), str(gds_path), str(_lyrdb_path)],
            capture_output=True,
            text=True,
            timeout=240,
        )
        _counts: dict[str, int] = {}
        if _lyrdb_path.exists():
            root = _ET.parse(_lyrdb_path).getroot()
            for item in root.findall(".//item"):
                cat = item.find("category")
                if cat is None or cat.text is None:
                    continue
                name = cat.text.strip("'")
                _counts[name] = _counts.get(name, 0) + 1
        _total = sum(_counts.values())
        _err = _result.stderr.strip()
        return _lyrdb_path, _total, _counts, _err

    def out_path(name: str) -> _Path:
        base = _Path(artifacts_dir.value).expanduser()
        base.mkdir(parents=True, exist_ok=True)
        safe_user = username.value.strip() or "user"
        return base / f"{safe_user}_{name}.gds"

    return out_path, run_drc


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            """
            ### Circuit 1: Si width violation (too narrow)
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    # TODO: Fix this by increasing width_um until DRC is clean.
    width_um = mo.ui.slider(
        start=0.02,
        stop=0.5,
        value=0.05,
        step=0.01,
        label="Waveguide width (µm)",
        show_value=True,
    )
    make_c1 = mo.ui.button(
        value=0, label="Write Circuit 1 GDS", kind="success", on_click=lambda v: (v or 0) + 1
    )
    run_c1 = mo.ui.button(
        value=0, label="Run DRC (Circuit 1)", kind="warn", on_click=lambda v: (v or 0) + 1
    )
    mo.vstack([width_um, mo.hstack([make_c1, run_c1])])
    return make_c1, run_c1, width_um


@app.cell
def _(make_c1, mo, out_path, run_c1, run_drc, width_um):
    import gdsfactory as _gf

    _gds = out_path("c1_si_width")
    _display = mo.md("Click **Write Circuit 1 GDS** then **Run DRC (Circuit 1)**.")
    if make_c1.value > 0:
        _c = _gf.Component("c1_si_width")
        # Floorplan
        _c.add_polygon([(-100, -100), (100, -100), (100, 100), (-100, 100)], layer=(99, 0))
        # Intentionally narrow Si strip
        _w = float(width_um.value)
        _c.add_polygon([(-20, -_w / 2), (20, -_w / 2), (20, _w / 2), (-20, _w / 2)], layer=(1, 0))
        _c.write_gds(_gds)
        _display = mo.callout(mo.md(f"Wrote `{_gds}`"), kind="success")

    if run_c1.value > 0:
        _lyrdb, _total, _counts, _err = run_drc(_gds)
        if _err:
            _display = mo.callout(mo.md(f"DRC stderr:\n```\n{_err}\n```"), kind="warn")
        else:
            _display = mo.callout(
                mo.md(f"`{_gds}` → `{_lyrdb}` (items: **{_total}**) {_counts}"), kind="info"
            )

    _display
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            """
            ### Circuit 2: Si space violation (two waveguides too close)
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    # TODO: Fix this by increasing gap_um until DRC is clean.
    gap_um = mo.ui.slider(
        start=0.0,
        stop=0.5,
        value=0.03,
        step=0.01,
        label="Gap between waveguides (µm)",
        show_value=True,
    )
    make_c2 = mo.ui.button(
        value=0, label="Write Circuit 2 GDS", kind="success", on_click=lambda v: (v or 0) + 1
    )
    run_c2 = mo.ui.button(
        value=0, label="Run DRC (Circuit 2)", kind="warn", on_click=lambda v: (v or 0) + 1
    )
    mo.vstack([gap_um, mo.hstack([make_c2, run_c2])])
    return gap_um, make_c2, run_c2


@app.cell
def _(gap_um, make_c2, mo, out_path, run_c2, run_drc):
    import gdsfactory as _gf

    _gds = out_path("c2_si_space")
    _display = mo.md("Click **Write Circuit 2 GDS** then **Run DRC (Circuit 2)**.")
    if make_c2.value > 0:
        _c = _gf.Component("c2_si_space")
        _c.add_polygon([(-100, -100), (100, -100), (100, 100), (-100, 100)], layer=(99, 0))
        _w = 0.5
        _gap = float(gap_um.value)
        # Two parallel Si strips separated by gap < min
        _y0 = -(_gap / 2 + _w / 2)
        _y1 = +(_gap / 2 + _w / 2)
        _c.add_polygon([(-20, _y0 - _w / 2), (20, _y0 - _w / 2), (20, _y0 + _w / 2), (-20, _y0 + _w / 2)], layer=(1, 0))
        _c.add_polygon([(-20, _y1 - _w / 2), (20, _y1 - _w / 2), (20, _y1 + _w / 2), (-20, _y1 + _w / 2)], layer=(1, 0))
        _c.write_gds(_gds)
        _display = mo.callout(mo.md(f"Wrote `{_gds}`"), kind="success")

    if run_c2.value > 0:
        _lyrdb, _total, _counts, _err = run_drc(_gds)
        if _err:
            _display = mo.callout(mo.md(f"DRC stderr:\n```\n{_err}\n```"), kind="warn")
        else:
            _display = mo.callout(
                mo.md(f"`{_gds}` → `{_lyrdb}` (items: **{_total}**) {_counts}"), kind="info"
            )

    _display
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            """
            ### Circuit 3: PinRec not inside Si (connectivity warning)
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    # TODO: Fix this by moving pin_offset_um to 0 so PinRec sits on the Si strip.
    pin_offset_um = mo.ui.slider(
        start=-5.0,
        stop=5.0,
        value=2.0,
        step=0.5,
        label="PinRec Y offset from waveguide center (µm)",
        show_value=True,
    )
    make_c3 = mo.ui.button(
        value=0, label="Write Circuit 3 GDS", kind="success", on_click=lambda v: (v or 0) + 1
    )
    run_c3 = mo.ui.button(
        value=0, label="Run DRC (Circuit 3)", kind="warn", on_click=lambda v: (v or 0) + 1
    )
    mo.vstack([pin_offset_um, mo.hstack([make_c3, run_c3])])
    return make_c3, pin_offset_um, run_c3


@app.cell
def _(make_c3, mo, out_path, pin_offset_um, run_c3, run_drc):
    import gdsfactory as _gf

    _gds = out_path("c3_pinrec")
    _display = mo.md("Click **Write Circuit 3 GDS** then **Run DRC (Circuit 3)**.")
    if make_c3.value > 0:
        _c = _gf.Component("c3_pinrec")
        _c.add_polygon([(-100, -100), (100, -100), (100, 100), (-100, 100)], layer=(99, 0))
        # Si waveguide
        _w = 0.5
        _c.add_polygon([(-20, -_w / 2), (20, -_w / 2), (20, _w / 2), (-20, _w / 2)], layer=(1, 0))
        # PinRec misplaced (not inside Si)
        _py = float(pin_offset_um.value)
        _c.add_polygon([(-2, _py - 0.25), (2, _py - 0.25), (2, _py + 0.25), (-2, _py + 0.25)], layer=(1, 10))
        # DevRec (optional, for realism)
        _c.add_polygon([(-25, -5), (25, -5), (25, 5), (-25, 5)], layer=(68, 0))
        _c.write_gds(_gds)
        _display = mo.callout(mo.md(f"Wrote `{_gds}`"), kind="success")

    if run_c3.value > 0:
        _lyrdb, _total, _counts, _err = run_drc(_gds)
        if _err:
            _display = mo.callout(mo.md(f"DRC stderr:\n```\n{_err}\n```"), kind="warn")
        else:
            _display = mo.callout(
                mo.md(f"`{_gds}` → `{_lyrdb}` (items: **{_total}**) {_counts}"), kind="info"
            )

    _display
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="submit"></a>
            ## Submission

            Submit:
            - Your cleaned HW02 GDS + .lyrdb (after fixes).
            - The broken + fixed versions of the 3 circuits from Part B (GDS + .lyrdb).
            - A short writeup describing how you diagnosed and fixed each error.
            """
        ).strip()
    )
    return


if __name__ == "__main__":
    app.run()
