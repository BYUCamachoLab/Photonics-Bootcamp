#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#   "marimo>=0.18.0",
#   "pyzmq",
#   "simphony==0.7.3",
#   "jax[cpu]",
#   "sax",
#   "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.19.6"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from _assignment_template import _ensure_lessons_on_path, load_lesson_template

    from textwrap import dedent as _dedent

    _ensure_lessons_on_path()
    inject_css, _make_doc_helpers, _make_health_refresh_button, header = load_lesson_template()
    inject_css(mo)

    header(
        mo,
        title="HW04 — Ring resonators (Simphony + design)",
        subtitle=(
            "Simulate ring resonators, measure FSR and Q, and design an add-drop ring."
        ),
        badges=["Week 4", "Homework", "Rings", "Simphony"],
        toc=[
            ("Overview", "overview"),
            ("Part A — Simulate 3 radii + measure FSR", "part-a"),
            ("Part B — Design for target FSR + estimate m", "part-b"),
            ("Part C — Add-drop ring + critical coupling + Q", "part-c"),
            ("Part D — Layout add-drop filter + DRC", "part-d"),
            ("Submission", "submit"),
        ],
        build="2026-01-28",
    )

    mo.callout(mo.md("Problem set (no solutions)."), kind="info")

    mo.md(
        _dedent(
            r"""
            <a id="overview"></a>
            ## Overview

            Four tasks:
            1. Simulate a ring resonator (3 radii) and measure the FSR.
            2. Design a ring for a target FSR and estimate the mode number near 1550 nm.
            3. Design an add-drop ring, attempt critical coupling, and estimate Q.
            4. Lay out an add-drop filter with grating couplers and pass DRC.
            """
        ).strip()
    )
    return mo


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-a"></a>
            ## Part A — Simulate 3 radii, measure FSR

            Simulate an ideal all-pass ring resonator in Simphony for three radii.
            From the plots, measure the FSR near 1550 nm and compare to the analytic result from class.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            ### Part A deliverables

            - Plot transmission vs wavelength for 3 radii.
            - Report measured FSR for each radius.
            - Report analytic FSR for each radius and percent error.

            Helpful imports:

            ```python
            from jax import config
            config.update("jax_enable_x64", True)

            import jax.numpy as jnp
            import sax
            from simphony.libraries import ideal
            import matplotlib.pyplot as plt
            ```
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            Record your results in a table (R, measured FSR, analytic FSR, percent error).
            """
        ).strip()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-b"></a>
            ## Part B — Design for target FSR

            Pick a target FSR near 1550 nm. Choose a ring radius that meets it (first pass),
            then estimate the mode number near 1550 nm (m).
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            ### Part B deliverables

            - Target FSR and chosen radius.
            - Estimated m near 1550 nm (value + nearest integer).
            """
        ).strip()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-c"></a>
            ## Part C — Add-drop ring + critical coupling + Q

            Design an **add-drop ring resonator** and simulate both **through** and **drop** ports.

            Goals:
            - Adjust coupling to attempt **critical coupling** (largest on-resonance extinction in the through port).
            - Estimate the **loaded Q** from your simulated spectrum (from the linewidth).
            - Compare your measured Q to an analytic estimate from class.

            ### Part C deliverables

            - Through + drop spectra for your add-drop ring (axes labeled).
            - A short note describing how you tuned coupling and whether you achieved near-critical coupling.
            - Q from the plot and your analytic Q estimate (with assumptions stated).
            """
        ).strip()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-d"></a>
            ## Part D — Layout add-drop filter + DRC

            Lay out an **add-drop ring filter** with **grating couplers** (input, through, drop).
            Export a GDS and make sure it passes all DRC checks.

            ### Part D deliverables

            - GDS of your add-drop filter with grating couplers.
            - A DRC report showing 0 items.
            - A screenshot of the layout.
            """
        ).strip()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="submit"></a>
            ## Submission

            Submit your plots/calculations (Parts A, B, C) and your layout artifacts (Part D).
            """
        ).strip()
    )
    return


if __name__ == "__main__":
    app.run()
