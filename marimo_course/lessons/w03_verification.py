#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.17.0",
#   "numpy",
#   "openai==2.15.0",
#   "pydantic-ai==1.44.0",
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
    return doc_badges, doc_callout_list


@app.cell
def _(mo):
    from _notebook_template import make_section_tabs

    section_tabs, view_state, set_view = make_section_tabs(
        mo,
        options=("All", "Overview", "Verification", "Next"),
        value="All",
    )
    section_tabs
    return (view_state,)


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_verification = view in ["All", "Verification"]
    show_next = view in ["All", "Next"]
    return show_next, show_overview, show_verification, view


@app.cell
def _(doc_badges, show_next, show_overview, show_verification, view):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
            (
                "Flags: "
                f"overview={show_overview}, "
                f"verification={show_verification}, "
                f"next={show_next}"
            ),
        ]
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    from _style import header

    header(
        mo,
        title="Verifying the MZI layout",
        subtitle=(
            "Use the openEBL verification workflow to ensure your layout passes checks "
            "before you push to GitHub."
        ),
        badges=["Week 3", "Lab companion", "Verification", "openEBL workflow"],
        toc=[
            ("Overview", "overview"),
            ("Verification", "verification"),
            ("What’s next", "next"),
        ],
        build="2025-12-16",
    )
    return


@app.cell
def _(mo):
    from _notebook_template import make_health_refresh_button

    health_refresh = make_health_refresh_button(mo)
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    overview_md = mo.md(r"""
    <a id="overview"></a>
    ## Overview

    Week 2 helped you connect **ΔL ↔ FSR** and build basic intuition for an MZI spectrum.
    This week is about the **verification pipeline** that keeps your openEBL submission green.

    Week 2 references:
    - `marimo_course/lessons/w02_mzi_modelling.py` (rule-of-thumb, spectrum intuition)
    - `marimo_course/lessons/w02_pdk_mzi_layout.py` (PDK layout workflow + submission layers)
    """)

    definitions = doc_callout_list(
        "info",
        tag="Definitions",
        title="What we mean by verification",
        items=[
            "<strong>Verification</strong>: checking that the layout obeys PDK/openEBL rules so it passes automated checks "
            "(ports, labels, floorplan, DFT rules, and CI).",
        ],
    )

    goals = doc_callout_list(
        "info",
        tag="Goals (lab)",
        title="What you should be able to do by the end",
        ordered=True,
        items=[
            "Run a verification checklist before pushing to GitHub/openEBL.",
            "Understand why CI checks fail and how to debug them in KLayout.",
            "Validate DFT requirements (pitch, orientation, opt_in placement).",
        ],
    )

    submission_note = doc_callout_list(
        "warning",
        tag="Where do I submit work?",
        title="Lab companion vs homework",
        items=[
            "This notebook is a lab companion (guided workflow + checklists).",
            "Graded work should live in the week-aligned homework notebook (e.g., `marimo_course/assignments/hw03_...`).",
        ],
    )
    mo.vstack([overview_md, definitions, goals, submission_note])
    return


@app.cell
def _():
    import numpy as np
    return


@app.cell
def _(doc_callout_list, mo, show_verification):
    mo.stop(not show_verification)
    verification_md = mo.md(r"""
    <a id="verification"></a>
    ## Verification: before you push to GitHub/openEBL

    The openEBL workflow is unforgiving in a good way: it forces clean layouts and consistent conventions.
    This section is a checklist you can follow every time before committing.
    """)

    klayout_intro = doc_callout_list(
        "info",
        tag="KLayout primer",
        title="First-time verification workflow",
        ordered=True,
        items=[
            "Install KLayout + SiEPIC-EBeam PDK (see `marimo_course/README.md`).",
            "Open your exported GDS/OAS in KLayout.",
            "Load the EBeam technology (verify layers, DevRec/PinRec).",
            "Run verification: press **V** or use the SiEPIC menu for verification.",
            "Inspect the error markers and fix layout issues before pushing.",
        ],
    )

    checklist = doc_callout_list(
        "info",
        tag="Checklist",
        title="Pre-push verification (starter list)",
        ordered=True,
        items=[
            "Open the design in KLayout with the SiEPIC-EBeam PDK loaded.",
            "Confirm ports/pins/DevRec conventions match the PDK expectations.",
            "Run local verification (DRC/connectivity) if available; fix obvious geometry errors first.",
            "Confirm labels for automated measurements are present and correctly formatted (if required by the run).",
            "Export GDS/OAS and re-open it to sanity-check hierarchy and floorplan placement.",
            "Push to your fork and check GitHub Actions results; if failing, download artifacts and debug in KLayout.",
        ],
    )

    sizing_bridge = doc_callout_list(
        "info",
        tag="Week 2 → Verification",
        title="What to carry forward from Week 2",
        items=[
            "Keep the compact-model vs layout mismatch in mind (loss, splitter imbalance).",
            "Check that your PDK layout uses PDK cells and adds PinRec/DevRec/Floorplan/labels.",
        ],
    )

    dft_rules = doc_callout_list(
        "info",
        tag="DFT rules (EBeam)",
        title="Grating coupler + opt_in checks from DFT.xml",
        ordered=True,
        items=[
            "Grating couplers are vertically aligned on a **127 µm pitch**.",
            "Minimum grating-coupler spacing is **60 µm**.",
            "GC array orientation is **90°** (vertical array).",
            "At most **1** GC above the opt_in label and at most **2** below.",
            "GC orientation is **0°** for `ebeam_gc_te1550` and `ebeam_gc_tm1550`.",
            "opt_in label is within **10 µm** of the GC tip (cell origin).",
        ],
    )

    common_failures = doc_callout_list(
        "warning",
        tag="Common CI failures",
        title="Issues students hit most often",
        items=[
            "Missing or misaligned PinRec markers on external ports.",
            "GCs off the 127 µm pitch or wrong orientation for the DFT rules.",
            "Layout outside the floorplan or missing DevRec/Floorplan.",
            "Top-cell name mismatch or unintended extra top cells.",
            "Modified black-box cells (GCs) or renamed PDK cells.",
        ],
    )

    todo = doc_callout_list(
        "warning",
        tag="TODO",
        title="Fill in run-specific links",
        items=[
            "Add links to the specific openEBL run repository and its technical summary for this semester.",
            "Add screenshots of the CI failure modes students most often hit (missing pins, wrong cell names, floorplan issues).",
            "Confirm these DFT rules against `SiEPIC_EBeam_PDK_public/klayout/EBeam/DFT.xml` for the active PDK version.",
        ],
    )
    mo.vstack(
        [
            verification_md,
            klayout_intro,
            checklist,
            sizing_bridge,
            dft_rules,
            common_failures,
            todo,
        ]
    )
    return


@app.cell
def _(mo, show_next):
    mo.stop(not show_next)
    mo.md(r"""
    <a id="next"></a>
    ## What’s next

    - Layout details (routing discipline, PDK-accurate cells, floorplanning) continue in the Week 2/4 layout lessons.
    - Next week’s focus is making layouts more manufacturable: consistent routing, clear ports, and verification habits.

    **Suggested homework structure**
    - Students implement the ΔL/FSR calculator (no UI), choose a ΔL, and record a brief justification.
    - Students attach a screenshot of their spectrum from the lab notebook and a screenshot of their “green” CI checks.
    """)
    return


if __name__ == "__main__":
    app.run()
