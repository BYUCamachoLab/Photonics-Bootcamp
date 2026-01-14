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
    mo.md(r"""
    # HW02 — MZI modelling (FSR and ΔL)

    Companion lab notebook: `marimo_course/lessons/w02_mzi_modelling.py`

    Default band: **TE @ 1550 nm** (1310 nm is optional extension).

    **What to submit (minimal)**
    1. Your implemented `fsr_estimate_nm(...)` function.
    2. A chosen ΔL (µm) and predicted FSR (nm) near 1550 nm.
    3. A screenshot or saved image of an MZI spectrum (from the lab notebook) showing multiple fringes.
    4. A short paragraph explaining your ΔL choice (trade-offs and constraints).
    """)
    return


@app.function
def fsr_estimate_nm(*, wl0_nm: float, ng: float, delta_L_um: float) -> float | None:
    """
    Estimate the MZI free spectral range (FSR) in nm.

    Rule-of-thumb near wl0:
      FSR ≈ wl0^2 / (ng * ΔL)

    Unit convention for this homework:
      - wl0_nm: nm
      - delta_L_um: µm
      - return value: nm

    TODO (student): implement the formula and unit conversion.
    """
    if wl0_nm <= 0 or ng <= 0 or delta_L_um <= 0:
        return None
    return None


@app.cell
def _(mo):
    mo.md(r"""
    ## Task 1 — Implement `fsr_estimate_nm`

    Implement `fsr_estimate_nm` above, then run the simple checks below (next cell).

    **Expected order-of-magnitude**
    - With ΔL = 10 µm and ng ≈ 4.2 at 1550 nm, FSR should be on the order of **tens of nm** (≈ 50–60 nm).
    - Doubling ΔL should roughly halve the FSR.
    """)
    return


@app.cell
def _(mo):
    wl0_nm_check = 1550.0
    ng_check = 4.19

    delta_L_um_values = (10.0, 20.0, 50.0)
    md_str = ""
    for delta_L_um_i in delta_L_um_values:
        fsr_nm_i = fsr_estimate_nm(wl0_nm=wl0_nm_check, ng=ng_check, delta_L_um=delta_L_um_i)
        md_str += (
            f"- λ0={wl0_nm_check:.0f} nm, ng={ng_check:.2f}, ΔL={delta_L_um_i:.0f} µm → "
            f"FSR = `{fsr_nm_i}` nm\n"
        )

    mo.md(md_str)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Task 2 — Choose ΔL (a design decision)

    Pick a ΔL that gives a spectrum with multiple fringes over a measurement span near **1550 nm**.

    For this homework, assume:
    - center wavelength: **1550 nm**
    - measurement span: **60 nm** (adjust to match what you used in the lab notebook if different)
    - desired fringes visible across the span: **≥ 3**

    Edit the variables in the next cell to record your choice and justification.
    """)
    return


@app.cell
def _(mo):
    # === EDIT THIS CELL ===
    wl0_nm = 1550.0
    ng = 4.19
    measurement_span_nm = 60.0

    chosen_delta_L_um = 25.0
    justification = "Replace this with a short paragraph."

    # === DO NOT EDIT BELOW (unless you want to) ===
    predicted_fsr_nm = fsr_estimate_nm(wl0_nm=wl0_nm, ng=ng, delta_L_um=chosen_delta_L_um)
    fringes_est = (
        None
        if predicted_fsr_nm in (None, 0)
        else float(measurement_span_nm) / float(predicted_fsr_nm)
    )

    mo.md(
        "\n".join(
            [
                f"- Chosen ΔL: `{chosen_delta_L_um}` µm",
                f"- Predicted FSR: `{predicted_fsr_nm}` nm",
                f"- Estimated fringes across {measurement_span_nm:.0f} nm: `{fringes_est}`",
                "",
                f"**Justification:** {justification}",
            ]
        )
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Task 3 — Short reflection (edit this cell)

    Replace the bullets below with your answer:

    - How does your layout choice (ΔL) show up in the measured spectrum (FSR)?
    - Name one reason a measured spectrum might deviate from the ideal analytic model.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Optional extension (advanced) — 1310 nm

    Compare the predicted FSR at 1310 nm vs 1550 nm for the same ΔL.
    """)

    wl0_1550_nm = 1550.0
    wl0_1310_nm = 1310.0
    ng_ext = 4.19
    delta_L_um_ext = 25.0

    fsr_1550 = fsr_estimate_nm(wl0_nm=wl0_1550_nm, ng=ng_ext, delta_L_um=delta_L_um_ext)
    fsr_1310 = fsr_estimate_nm(wl0_nm=wl0_1310_nm, ng=ng_ext, delta_L_um=delta_L_um_ext)

    mo.md(
        f"With ΔL={delta_L_um_ext:.0f} µm and ng={ng_ext:.2f}: "
        f"FSR@1550 = `{fsr_1550}` nm, FSR@1310 = `{fsr_1310}` nm"
    )
    return


if __name__ == "__main__":
    app.run()
