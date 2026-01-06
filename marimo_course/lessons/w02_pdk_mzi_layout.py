#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.17.0",
#   "pyzmq",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    from _notebook_template import inject_css

    inject_css(mo)
    return


@app.cell
def _(mo):
    from _notebook_template import make_doc_helpers

    doc_badges, doc_callout_html, doc_callout_list = make_doc_helpers(mo)
    return doc_badges, doc_callout_html, doc_callout_list


@app.cell
def _(mo):
    from _notebook_template import make_section_tabs

    section_tabs, view_state, set_view = make_section_tabs(
        mo,
        options=("All", "Overview", "Targets", "KLayout + PDK", "Layout skeleton", "Submission"),
        value="All",
    )
    section_tabs
    return set_view, view_state


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_targets = view in ["All", "Targets"]
    show_klayout = view in ["All", "KLayout + PDK"]
    show_skeleton = view in ["All", "Layout skeleton"]
    show_submission = view in ["All", "Submission"]
    return (
        show_klayout,
        show_overview,
        show_skeleton,
        show_submission,
        show_targets,
        view,
    )


@app.cell
def _(doc_badges, view):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
        ]
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    from _style import header

    header(
        mo,
        title="PDK MZI layout (KLayout + SiEPIC)",
        subtitle=(
            "Build a first MZI layout using the SiEPIC-EBeam PDK workflow in KLayout. "
            "Use modelling targets (ΔL ↔ FSR) to guide geometry choices, then save your work in the openEBL repo."
        ),
        badges=["Week 2", "Lab companion", "PDK", "KLayout", "openEBL workflow"],
        toc=[
            ("Overview", "overview"),
            ("Targets", "targets"),
            ("KLayout + PDK", "klayout"),
            ("Layout skeleton", "skeleton"),
            ("Submission", "submission"),
        ],
        build="2025-12-16",
    )
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    <a id="overview"></a>
    ## Overview

    This is the **PDK + compact-model + layout** companion for Week 2. The modelling companion is:
    `marimo_course/lessons/w02_mzi_modelling.py`, where you derived and explored the ideal MZI transfer function.

    In this notebook, you’ll connect three ideas that show up in every photonics workflow:

    - **Compact models:** fast, circuit-level models of components (couplers, waveguides, phase shifters) that let you
      simulate a whole photonic circuit without solving Maxwell’s equations everywhere.
    - **PDK (process design kit):** a foundry/technology “package” that defines the **design rules**, **layers**, and
      **parameterized building blocks** (plus their compact models) so your design is manufacturable and checkable.
    - **Reproducibility across views:** build the *same* MZI you modelled last lesson, first as a **circuit** from compact
      models and then as a **layout** in KLayout using PDK cells.

    In lab, you will:

    1. Decide on a **target** (FSR → ΔL) near **1550 nm**.
    2. Build an MZI from **compact models** (component → circuit) and sanity-check it against the Week 2 model.
    3. Assemble the same MZI from **PDK building blocks** in KLayout (splitter, waveguides, combiner, I/O).
    4. Add the **conventions** required for downstream checks (ports/pins, DevRec, labels/floorplan as required).
    5. Save your design in the **openEBL** submission repo and keep CI green.
    """)

    doc_callout_list(
        "info",
        tag="Learning goals",
        title="What you should be able to do after this notebook",
        items=[
            "Explain what a compact model is and why we use them for circuit-level photonics design.",
            "Describe what a PDK provides (layers, rules, cells, models) and why it matters for manufacturable layouts.",
            "Create an MZI from compact-model building blocks and connect ΔL ↔ FSR back to the modelling notebook.",
            "Implement the same MZI in KLayout using PDK-accurate cells so it passes downstream checks.",
        ],
    )

    doc_callout_list(
        "warning",
        tag="Where is the graded work?",
        title="Lab companion vs homework",
        items=[
            "This notebook is a lab companion (workflow + checklists + reference).",
            "Graded work should live in a homework notebook under `marimo_course/assignments/`.",
        ],
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    klayout_open = mo.ui.checkbox(label="KLayout open with SiEPIC-EBeam PDK", value=False)
    placed_blocks = mo.ui.checkbox(label="Placed I/O + splitter/combiner cells", value=False)
    routed = mo.ui.checkbox(label="Routed an MZI skeleton with ΔL", value=False)
    annotated = mo.ui.checkbox(label="Added pins/DevRec/labels as required", value=False)
    saved = mo.ui.checkbox(label="Saved in openEBL repo + CI checked", value=False)
    mo.vstack([klayout_open, placed_blocks, routed, annotated, saved])
    return


@app.cell
def _(mo, set_view, show_overview):
    mo.stop(not show_overview)
    go_targets = mo.ui.button(
        value=0,
        kind="success",
        label="Go to Targets",
        on_click=lambda v: (set_view("Targets"), (v or 0) + 1)[-1],
    )
    go_klayout = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to KLayout + PDK",
        on_click=lambda v: (set_view("KLayout + PDK"), (v or 0) + 1)[-1],
    )
    go_skeleton = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to Layout skeleton",
        on_click=lambda v: (set_view("Layout skeleton"), (v or 0) + 1)[-1],
    )
    go_submission = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to Submission",
        on_click=lambda v: (set_view("Submission"), (v or 0) + 1)[-1],
    )
    mo.hstack([go_targets, go_klayout, go_skeleton, go_submission], justify="start", gap=1)
    return


@app.cell
def _(doc_callout_html, mo, show_targets):
    mo.stop(not show_targets)
    mo.md(r"""
    <a id="targets"></a>
    ## Targets: pick ΔL from an FSR target (1550 nm default)

    Use the Week 2 modelling notebook to build intuition and sanity-check values:
    `marimo_course/lessons/w02_mzi_modelling.py`.

    Rule-of-thumb near λ0:

    $$
    \mathrm{FSR} \approx \frac{\lambda_0^2}{n_g\,\Delta L}.
    $$
    """)

    doc_callout_html(
        "info",
        tag="Tip",
        title="What matters for FSR",
        html=(
            "- ΔL sets fringe spacing (FSR) approximately as `1/ΔL`.\n"
            "- Base length doesn’t change FSR in the ideal model.\n"
            "- Use **1550 nm** by default; treat **1310 nm** as an extension."
        ),
    )
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    wl0_nm = mo.ui.number(value=1550.0, label="λ0 (nm)")
    ng = mo.ui.number(value=4.19, label="ng (group index)")
    deltaL_um = mo.ui.number(value=50.0, label="Planned ΔL (µm)")
    mo.hstack([wl0_nm, ng, deltaL_um])
    return deltaL_um, ng, wl0_nm


@app.cell
def _(deltaL_um, mo, ng, show_targets, wl0_nm):
    mo.stop(not show_targets)
    wl0_um = float(wl0_nm.value) / 1e3
    ng_val = float(ng.value)
    delta_L_um = float(deltaL_um.value)
    fsr_nm = (
        None
        if (delta_L_um <= 0 or ng_val <= 0)
        else (wl0_um * wl0_um) / (ng_val * delta_L_um) * 1e3
    )
    mo.md(
        "FSR estimate: (enter positive ΔL and ng)"
        if fsr_nm is None
        else f"FSR estimate: **{fsr_nm:.2f} nm**"
    )
    return


@app.cell
def _(deltaL_um, mo, show_targets):
    mo.stop(not show_targets)
    import base64 as b64

    delta_L_um_vis = float(deltaL_um.value)
    extra = max(0.0, min(80.0, delta_L_um_vis))  # purely visual; does not affect calculations
    dy = 26
    x0, x1, x2, x3 = 20, 110, 310, 400
    y_mid = 65
    y_top = y_mid - dy
    y_bot = y_mid + dy

    # The upper arm is drawn a bit longer (extra) to visually suggest ΔL.
    x2_top = x2 + extra

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="520" height="140" viewBox="0 0 520 140">
      <style>
        .wg {{ fill: none; stroke: #111; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
        .box {{ fill: #f6f6f6; stroke: #999; stroke-width: 1.5; }}
        .txt {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; font-size: 12px; fill: #111; }}
        .sub {{ font-size: 11px; fill: #444; }}
      </style>

      <!-- input / output -->
      <path class="wg" d="M {x0} {y_mid} L {x1} {y_mid}" />
      <path class="wg" d="M {x3} {y_mid} L 500 {y_mid}" />

      <!-- coupler boxes -->
      <rect class="box" x="{x1}" y="{y_mid-18}" width="70" height="36" rx="6"/>
      <rect class="box" x="{x3-70}" y="{y_mid-18}" width="70" height="36" rx="6"/>
      <text class="txt" x="{x1+10}" y="{y_mid-2}">Splitter</text>
      <text class="txt" x="{x3-60}" y="{y_mid-2}">Combiner</text>

      <!-- arms -->
      <path class="wg" d="M {x1+70} {y_top} L {x2_top} {y_top} L {x3-70} {y_top}" />
      <path class="wg" d="M {x1+70} {y_bot} L {x2} {y_bot} L {x3-70} {y_bot}" />
      <path class="wg" d="M {x1+70} {y_mid} L {x1+70} {y_top}" />
      <path class="wg" d="M {x1+70} {y_mid} L {x1+70} {y_bot}" />
      <path class="wg" d="M {x3-70} {y_mid} L {x3-70} {y_top}" />
      <path class="wg" d="M {x3-70} {y_mid} L {x3-70} {y_bot}" />

      <!-- labels -->
      <text class="txt" x="20" y="20">Circuit schematic (conceptual)</text>
      <text class="txt sub" x="20" y="38">Upper arm longer by ΔL ≈ {delta_L_um_vis:.1f} µm (visual only)</text>
    </svg>
    """.strip()

    svg_b64 = b64.b64encode(svg.encode("utf-8")).decode("ascii")
    mo.md(
        "<div style='max-width:100%; overflow:auto;'>"
        f"<img src='data:image/svg+xml;base64,{svg_b64}' style='max-width:100%; height:auto;'/>"
        "</div>"
    )
    return


@app.cell
def _(doc_callout_list, mo, show_klayout):
    mo.stop(not show_klayout)
    mo.md(r"""
    <a id="klayout"></a>
    ## KLayout + SiEPIC-EBeam PDK setup

    This section is intentionally procedural: the goal is to reduce “where do I click?” friction in lab.
    """)

    doc_callout_list(
        "info",
        tag="Checklist",
        title="Setup and sanity checks",
        ordered=True,
        items=[
            "Install KLayout and the SiEPIC-EBeam PDK (confirm the technology loads).",
            "Confirm the correct process/run assumptions for this semester (default: **1550 nm** structures).",
            "Open an example layout from the PDK and verify layers look sensible.",
            "Create a new layout inside the run repo using the required filename conventions.",
        ],
    )
    return


@app.cell
def _(doc_callout_list, mo, show_skeleton):
    mo.stop(not show_skeleton)
    mo.md(r"""
    <a id="skeleton"></a>
    ## Layout skeleton (MZI) — build first, refine later

    Build a simple MZI skeleton using PDK cells (splitter/combiner + waveguides + I/O).
    Keep it **simple and clean**: symmetry, straight segments where possible, and a clear way to implement ΔL.

    Optional: generate a quick “geometry-only” MZI skeleton using gdsfactory to visualize the idea,
    then recreate it with PDK-accurate cells in KLayout.
    """)

    doc_callout_list(
        "warning",
        tag="Important",
        title="PDK vs generic geometry",
        items=[
            "For openEBL submissions, your final design must follow the PDK cell conventions expected by the run repo.",
            "A gdsfactory skeleton is useful for intuition, but it is not a substitute for a PDK-accurate KLayout design.",
        ],
    )
    return


@app.cell
def _(mo, show_skeleton):
    mo.stop(not show_skeleton)
    from _notebook_template import optional_import

    gf_mod, gf_error = optional_import("gdsfactory")
    available = gf_mod is not None

    doc = (
        "Optional gdsfactory helper: **available**"
        if available
        else f"Optional gdsfactory helper: **not available** (`{gf_error}`)"
    )
    mo.md(doc)
    return available, gf_mod


@app.cell
def _(available, mo, show_skeleton):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    gds_out = mo.ui.text(value="marimo_course/build/week2_mzi_skeleton.gds", label="GDS output path")
    delta_length = mo.ui.number(value=50.0, label="ΔL (µm)")
    length_x = mo.ui.number(value=60.0, label="length_x (µm)")
    length_y = mo.ui.number(value=10.0, label="length_y (µm)")
    write = mo.ui.button(value=0, label="Write GDS", kind="success", on_click=lambda v: (v or 0) + 1)
    mo.vstack([mo.hstack([gds_out, write]), mo.hstack([delta_length, length_x, length_y])])
    return


@app.cell
def _(available, gf_mod, mo, show_skeleton):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    from pathlib import Path

    def write_mzi_skeleton(*, out: Path, delta_length_um: float, length_x_um: float, length_y_um: float) -> Path:
        gf = gf_mod
        mzi = gf.components.mzi(
            delta_length=float(delta_length_um),
            length_x=float(length_x_um),
            length_y=float(length_y_um),
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        written = mzi.write_gds(gdspath=out)
        return Path(written)
    return Path, write_mzi_skeleton


@app.cell
def _(
    Path,
    available,
    delta_length,
    gds_out,
    length_x,
    length_y,
    mo,
    show_skeleton,
    write,
    write_mzi_skeleton,
):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    blocks = []
    if int(write.value or 0) <= 0:
        blocks.append(
            mo.md("Click **Write GDS** to export a skeleton you can inspect in KLayout.")
        )
    else:
        out = Path(str(gds_out.value)).expanduser()
        try:
            written = write_mzi_skeleton(
                out=out,
                delta_length_um=float(delta_length.value),
                length_x_um=float(length_x.value),
                length_y_um=float(length_y.value),
            )
            blocks.append(mo.md(f"Wrote: `{written}`"))
            blocks.append(mo.md(f"Open in KLayout: `klayout {written}`"))
        except Exception as e:  # pragma: no cover
            blocks.append(mo.md(f"(GDS write failed: `{type(e).__name__}: {e}`)"))

    mo.vstack(blocks)
    return


@app.cell
def _(doc_callout_list, mo, show_submission):
    mo.stop(not show_submission)
    mo.md(r"""
    <a id="submission"></a>
    ## Save + submission workflow (openEBL)

    The details depend on the specific openEBL run repository used this semester, but the structure is consistent:
    save designs in the right folder, run checks, fix failures, and submit via PR.
    """)

    doc_callout_list(
        "info",
        tag="Checklist",
        title="Before you push",
        ordered=True,
        items=[
            "Confirm your layout file is inside the run repo (e.g., `openEBL-2026-02/submissions/...`).",
            "Verify naming conventions and top-level cell structure match the run instructions.",
            "Run local verification in KLayout if available (press V / run scripts).",
            "Push to your fork and check GitHub Actions results; download artifacts when something fails.",
        ],
    )
    return


if __name__ == "__main__":
    app.run()
