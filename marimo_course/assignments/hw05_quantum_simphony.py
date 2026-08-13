#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#   "marimo>=0.18.4",
#   "pyzmq",
#   "simphony==0.7.3",
#   "jax[cpu]",
#   "sax",
#   "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.21.1"
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
        title="HW05 — Converting classical Simphony models to quantum Simphony",
        subtitle="A line-by-line assignment on turning field-amplitude simulations into Gaussian quantum simulations.",
        badges=["Week 10", "Homework", "Quantum optics", "Simphony"],
        toc=[
            ("Overview", "overview"),
            ("Part A — Coupler conversion", "part-a"),
            ("Part B — Add squeezing", "part-b"),
            ("Part C — MZI conversion", "part-c"),
            ("Part D — Reflection", "part-d"),
            ("Submission", "submit"),
        ],
        build="2026-03-25",
    )

    mo.callout(mo.md("Problem set (no solutions)."), kind="info")

    mo.md(
        _dedent(
            r"""
            <a id="overview"></a>
            ## Overview

            This assignment is about a **workflow conversion**, not a new device:

            1. Start from a classical Simphony model you already understand.
            2. Replace the classical input/output logic with a Gaussian quantum simulation.
            3. Compare what stays the same and what new information appears.

            Your goal is to learn how to go from:

            - classical **field amplitudes** and **power**, to
            - quantum **means**, **variances**, and **covariances**.

            Companion lesson notebook:
            `marimo_course/lessons/w10_gaussian_quantum_optics.py`
            """
        ).strip()
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-a"></a>
            ## Part A — Convert a coupler simulation line by line

            Start from the classical coupler workflow:

            1. build a circuit,
            2. choose an input amplitude,
            3. run the circuit,
            4. inspect the output amplitudes or powers.

            Now convert it into a **coherent-state quantum simulation**.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part A instructions: exact replacements

    Suppose your classical code looked roughly like this:

    ```python
    import jax.numpy as jnp
    import sax
    from simphony.libraries import ideal

    circuit = build_coupler_circuit()
    wl_um = jnp.array([1.55])
    S = circuit(
        wl=wl_um,
        dc={"coupling": 0.5, "loss": 0.0, "phi": 0.5 * np.pi},
    )

    a_in = jnp.array([1.0 + 0.0j, 0.0 + 0.0j])
    a_out = S @ a_in
    power_out = jnp.abs(a_out) ** 2
    ```

    Replace it **line by line** as follows:

    1. Keep the circuit definition the same.
    2. Keep the wavelength array the same.
    3. Replace the classical scattering call with `QuantumSim(...)`.
    4. Replace `a_in` with `compose_qstate(CoherentState("in0", alpha), vacuum_state("in1"))`.
    5. Replace `a_out` with `result.state(0)` and then call `to_xpxp()`.
    6. Replace the output amplitude readout with `output_state.modes(mode_index)`.
    7. Report:
       - output mean `X`,
       - output mean `P`,
       - output variance `Var(X)`,
       - output variance `Var(P)`.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part A deliverables

    - A short code cell that builds and runs a quantum coupler simulation for a coherent input.
    - A table for `out0` and `out1` containing:
      - `mean_X`
      - `mean_P`
      - `var_X`
      - `var_P`
    - One sentence explaining what matches the classical coupler result and what new information the quantum simulation adds.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part A starter imports

    Use these imports in your implementation:

    ```python
    from jax import config
    config.update("jax_enable_x64", True)

    import jax.numpy as jnp
    import matplotlib.pyplot as plt
    import sax
    from simphony.libraries import ideal
    from simphony.quantum import CoherentState, QuantumSim, compose_qstate
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part A student work cell

    Edit this cell. Follow the replacement checklist above.
    """)
    return


@app.cell
def _(mo):
    # === EDIT THIS CELL ===
    part_a_notes = """
    Replace this text with:
    - your Part A code summary,
    - your output table,
    - one sentence comparing classical vs quantum coupler outputs.
    """
    # === END EDIT ===

    mo.md(part_a_notes)
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-b"></a>
            ## Part B — Keep the mean field, add squeezing

            In Part A, the input was a coherent state.

            Now keep the **same displaced mean field**, but replace the coherent input with a
            **displaced squeezed state**.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part B instructions: exact replacements

    Start from your coherent-state quantum code from Part A.

    Replace this line:

    ```python
    CoherentState("in0", alpha)
    ```

    with this line:

    ```python
    SqueezedState("in0", r=r_value, phi=np.deg2rad(phi_deg), alpha=alpha)
    ```

    Then:

    1. Keep the same circuit.
    2. Keep the same input displacement `alpha`.
    3. Choose a nonzero squeezing strength `r`.
    4. Choose a squeezing angle `phi`.
    5. Compare the output covariance matrix to the coherent-state covariance.

    Focus on this question:
    **Does the mean move, or does the uncertainty change?**
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part B deliverables

    - One coherent-state output covariance matrix.
    - One squeezed-state output covariance matrix.
    - A short note identifying which quadrature got quieter and which got noisier.
    - One sentence explaining why the mean output can stay similar while the sensing performance changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-c"></a>
            ## Part C — Convert a classical MZI sensing script into a quantum sensing script

            This is the main workflow conversion.

            You will take a classical MZI sweep over a perturbation and rewrite it as a quantum sweep.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part C classical reference pattern

    A classical sensing script often looks like this:

    ```python
    for delta_neff in delta_neff_values:
        S = mzi_circuit(...)
        a_in = ...
        a_out = S @ a_in
        signal.append(...)
    ```

    The quantum version should look like this:

    ```python
    for delta_neff in delta_neff_values:
        sim = QuantumSim(...)
        qstate_in = compose_qstate(...)
        sim.add_qstate(qstate_in)
        output_state = sim.run().state(0)
        output_state.to_xpxp()
        means, cov = output_state.modes(port_index)
        # record means and covariances
    ```
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part C line-by-line checklist

    Use this exact sequence:

    1. Keep the **MZI circuit topology** unchanged.
    2. Keep the **parameter sweep** (`delta_neff_values`) unchanged.
    3. Replace the classical scattering evaluation with `QuantumSim(...)`.
    4. Replace the classical input vector with:
       - `CoherentState(...)` for the baseline case,
       - `SqueezedState(...)` for the quantum-enhanced case.
    5. After `sim.run()`, call:

       ```python
       output_state = result.state(0)
       output_state.to_xpxp()
       means, cov = output_state.modes(port_index)
       ```

    6. Record the following quantities versus `delta_neff`:
       - output mean,
       - output variance,
       - any sensing proxy you choose, such as
         `sigma / |d(signal)/d(delta_neff)|`.

    7. Plot the coherent and squeezed sensing limits on the same axes.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part C deliverables

    - A plot of the coherent and squeezed sensing curves.
    - A short description of your sensing proxy.
    - The best coherent limit you found.
    - The best squeezed limit you found.
    - An improvement factor:
      `coherent_limit / squeezed_limit`.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Part C student work cell

    Replace the placeholder text below with your own implementation notes and results.
    """)
    return


@app.cell
def _(mo):
    # === EDIT THIS CELL ===
    part_c_notes = """
    Replace this text with:
    - your MZI conversion steps,
    - your sensing proxy definition,
    - your coherent and squeezed results,
    - your improvement factor.
    """
    # === END EDIT ===

    mo.md(part_c_notes)
    return


@app.cell(hide_code=True)
def _(mo):
    from textwrap import dedent as _dedent

    mo.md(
        _dedent(
            r"""
            <a id="part-d"></a>
            ## Part D — Reflection

            Answer the following in complete sentences.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    1. Which lines of a classical Simphony workflow stayed essentially unchanged when you moved to the quantum version?
    2. Which lines had to be replaced completely?
    3. What new physical information does the quantum simulation return that the classical one does not?
    4. Why can squeezing help sensing even when the average signal looks similar?
    """)
    return


@app.cell
def _(mo):
    # === EDIT THIS CELL ===
    reflection = """
    Replace this block with your Part D reflection answers.
    """
    # === END EDIT ===

    mo.md(reflection)
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

            - your completed notebook,
            - your Part A coupler comparison,
            - your Part B covariance comparison,
            - your Part C MZI sensing plot + improvement factor,
            - your Part D reflection.
            """
        ).strip()
    )
    return


if __name__ == "__main__":
    app.run()
