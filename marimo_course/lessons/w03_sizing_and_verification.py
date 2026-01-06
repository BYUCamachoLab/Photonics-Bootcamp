#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.17.0",
#   "numpy",
#   "pyzmq",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


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
        options=("All", "Overview", "Sizing", "Verification", "Next"),
        value="All",
    )
    section_tabs
    return (view_state,)


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_sizing = view in ["All", "Sizing"]
    show_verification = view in ["All", "Verification"]
    show_next = view in ["All", "Next"]
    return show_next, show_overview, show_sizing, show_verification, view


@app.cell
def _(
    doc_badges,
    show_next,
    show_overview,
    show_sizing,
    show_verification,
    view,
):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
            (
                "Flags: "
                f"overview={show_overview}, "
                f"sizing={show_sizing}, "
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
        title="Sizing and verifying the MZI",
        subtitle=(
            "Turn a modelling target (FSR, extinction, loss) into concrete layout parameters, "
            "then run the checks that keep your openEBL submission green."
        ),
        badges=["Week 3", "Lab companion", "Sizing", "Verification", "openEBL workflow"],
        toc=[
            ("Overview", "overview"),
            ("Sizing", "sizing"),
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
    return (health_refresh,)


@app.cell
def _(doc_callout_html, health_refresh, mo):
    from _notebook_template import safe_editing_panel

    safe_editing_panel(
        mo,
        doc_callout_html,
        health_refresh,
        restore_command="git -C Photonics-Bootcamp restore marimo_course/lessons/w03_sizing_and_verification.py",
        external_check_command="python3 marimo_course/lessons/check_notebook_health.py marimo_course/lessons/w03_sizing_and_verification.py",
    )
    return


@app.cell
def _(doc_badges, doc_callout_html, health_refresh):
    from _notebook_template import notebook_self_check_view

    _self_check_view = notebook_self_check_view(
        doc_badges=doc_badges,
        doc_callout_html=doc_callout_html,
        notebook_path=__file__,
        refresh_token=health_refresh.value,
    )
    _self_check_view
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    <a id="overview"></a>
    ## Overview

    Week 2 helped you connect **ΔL ↔ FSR** and build basic intuition for an MZI spectrum.
    This week is about translating that intuition into **design choices** and then passing the
    **verification pipeline** for openEBL.
    """)

    doc_callout_list(
        "info",
        tag="Goals (lab)",
        title="What you should be able to do by the end",
        ordered=True,
        items=[
            "Choose a target FSR and compute a corresponding ΔL (rule-of-thumb).",
            "Recognize which parameters change fringe spacing vs fringe contrast (qualitatively).",
            "Run a verification checklist before pushing to GitHub/openEBL.",
        ],
    )

    doc_callout_list(
        "warning",
        tag="Where do I submit work?",
        title="Lab companion vs homework",
        items=[
            "This notebook is a lab companion (guided workflow + checklists).",
            "Graded work should live in the week-aligned homework notebook (e.g., `marimo_course/assignments/hw03_...`).",
        ],
    )
    return


@app.cell
def _(doc_callout_html, mo, show_sizing):
    mo.stop(not show_sizing)
    mo.md(r"""
    <a id="sizing"></a>
    ## Sizing: choose ΔL from an FSR target

    The Week 2 rule-of-thumb (near λ0) is:

    $$
    \mathrm{FSR} \approx \frac{\lambda_0^2}{n_g \, \Delta L}.
    $$

    Use it to pick a ΔL that gives enough fringes over a measurement span without making fringes so dense
    that they’re hard to measure.
    """)

    doc_callout_html(
        "info",
        tag="Rule of thumb",
        title="What changes what?",
        html=r"""
        <ul>
          <li><strong>Fringe spacing (FSR):</strong> mainly set by ΔL (and ng).</li>
          <li><strong>Fringe contrast (visibility):</strong> affected by loss imbalance and non-ideal splitters.</li>
          <li><strong>Absolute phase:</strong> shifts fringes left/right but does not change spacing.</li>
        </ul>
        """,
    )
    return


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _(mo, np, show_sizing):
    mo.stop(not show_sizing)

    wl0_nm = mo.ui.number(value=1550.0, label="λ0 (nm, default 1550)")
    ng = mo.ui.number(value=4.19, label="ng (group index)")
    target_fsr_nm = mo.ui.number(value=25.0, label="Target FSR (nm)")

    wl0_um = float(wl0_nm.value) / 1e3
    fsr_nm = float(target_fsr_nm.value)
    ng_val = float(ng.value)

    deltaL_um = None
    if fsr_nm > 0 and ng_val > 0:
        deltaL_um = (wl0_um * wl0_um) / (ng_val * (fsr_nm / 1e3))

    text = (
        f"ΔL estimate: **{deltaL_um:.1f} µm**"
        if isinstance(deltaL_um, float) and np.isfinite(deltaL_um)
        else "ΔL estimate: (enter positive `ng` and `FSR`)"
    )
    mo.vstack([mo.hstack([wl0_nm, ng, target_fsr_nm]), mo.md(text)])
    return


@app.cell
def _(doc_callout_list, mo, show_verification):
    mo.stop(not show_verification)
    mo.md(r"""
    <a id="verification"></a>
    ## Verification: before you push to GitHub/openEBL

    The openEBL workflow is unforgiving in a good way: it forces clean layouts and consistent conventions.
    This section is a checklist you can follow every time before committing.
    """)

    doc_callout_list(
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

    doc_callout_list(
        "warning",
        tag="TODO",
        title="Fill in run-specific links",
        items=[
            "Add links to the specific openEBL run repository and its technical summary for this semester.",
            "Add screenshots of the CI failure modes students most often hit (missing pins, wrong cell names, floorplan issues).",
        ],
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
