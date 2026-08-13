#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#   "marimo>=0.17.0",
#   "pyzmq",
#   "simphony==0.7.3",
#   "jax[cpu]",
#   "sax",
#   "matplotlib",
#   "gdsfactory",
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
    <style>
    .pb-callout {
      border-left: 4px solid rgba(31, 111, 235, 0.9);
      background: rgba(31, 111, 235, 0.08);
      padding: 10px 12px;
      border-radius: 10px;
      margin: 12px 0;
    }
    </style>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Week 4 (Mon) - Ring resonators

    <div class="pb-callout">
    This week shifts from "one main device" (MZI) to adding other useful structures.
    Today's focus is the <strong>ring resonator</strong>: what it does, what knobs you can tune,
    and what a "good" layout looks like.
    </div>

    ## Goals
    - Explain the ring resonance condition and the meaning of FSR and Q.
    - Given a target wavelength band, pick a first-pass ring radius that gives a reasonable FSR.
    - Identify coupling regimes (under / critical / over) and what they do to the lineshape.
    - Sketch a clean "bus + ring" floorplan that is easy to probe and easy to route.

    ## In-class checklist
    - [ ] Use the calculator below to pick a radius that gives the FSR you want near 1550 nm.
    - [ ] Decide: all-pass ring (through only) or add-drop ring (through + drop).
    - [ ] Choose a coupling gap (and coupling length, if used) that is plausible for the PDK.
    - [ ] Place I/O structures and keep straight access waveguides near grating couplers.
    - [ ] Add/verify labels for device name / metadata (as required).

    ## Reference equations (first-pass)
    Let the ring have radius <code>R</code> and round-trip length <code>L = 2πR</code>.

    - Resonance condition (conceptual): <code>m λ ≈ n_eff L</code>
    - FSR in wavelength (approx near λ0): <code>FSR_λ ≈ λ0^2 / (n_g L)</code>
    - Intrinsic Q from propagation loss (rough): <code>Q_i ≈ (2π n_g) / (α λ0)</code>

    where <code>n_g</code> is group index and <code>α</code> is power attenuation (Np/m).

    ## Common layout pitfalls (watch for these)
    - Ring too small: bend loss dominates, and the spectrum looks "washed out".
    - No straight access sections: hard to probe and harder to measure consistently.
    - Coupling gap too aggressive: coupling becomes very fabrication-sensitive.
    - Ugly floorplan: long, unnecessary routing adds loss and hides the intent of the design.
    """)
    return


@app.cell
def _():
    import math
    return (math,)


@app.cell
def _(mo):
    radius_um = mo.ui.slider(
        start=2.0,
        stop=50.0,
        step=0.5,
        value=10.0,
        label="Ring radius R (um)",
    )
    ng = mo.ui.slider(
        start=2.0,
        stop=5.0,
        step=0.05,
        value=4.0,
        label="Group index n_g (unitless)",
    )
    lambda0_nm = mo.ui.slider(
        start=1500.0,
        stop=1600.0,
        step=0.5,
        value=1550.0,
        label="Center wavelength lambda0 (nm)",
    )
    loss_db_per_cm = mo.ui.slider(
        start=0.0,
        stop=10.0,
        step=0.1,
        value=2.0,
        label="Propagation loss (dB/cm) (optional)",
    )
    mo.vstack([radius_um, ng, lambda0_nm, loss_db_per_cm])
    return lambda0_nm, loss_db_per_cm, ng, radius_um


@app.cell
def _(lambda0_nm, loss_db_per_cm, math, mo, ng, radius_um):
    R_um = float(radius_um.value)
    ng_value = float(ng.value)
    lambda0_nm_value = float(lambda0_nm.value)
    loss_db_per_cm_value = float(loss_db_per_cm.value)

    L_um = 2.0 * math.pi * R_um
    lambda0_um = lambda0_nm_value * 1e-3

    # FSR_lambda ~= lambda0^2 / (ng * L)
    fsr_um = (lambda0_um**2) / (ng_value * L_um)
    fsr_nm = fsr_um * 1e3

    # Optional intrinsic Q estimate from propagation loss.
    # Convert loss from dB/cm -> dB/m -> Np/m (power attenuation).
    # alpha_np_per_m = (loss_db_per_m) * ln(10) / 10
    loss_db_per_m = loss_db_per_cm_value * 100.0
    alpha_np_per_m = loss_db_per_m * math.log(10.0) / 10.0
    lambda0_m = lambda0_nm_value * 1e-9
    qi = (2.0 * math.pi * ng_value) / (alpha_np_per_m * lambda0_m) if alpha_np_per_m > 0 else float("inf")

    qi_text = (
        f"{qi:,.0f} (rough)"
        if math.isfinite(qi)
        else "infinite (loss = 0 dB/cm)"
    )

    mo.md(
        f"""
        ## Quick calculator (FSR + rough intrinsic Q)

        Using:
        - R = **{R_um:.1f} um**  ->  L = 2*pi*R = **{L_um:.1f} um**
        - n_g = **{ng_value:.2f}**
        - lambda0 = **{lambda0_nm_value:.1f} nm**

        First-pass results:
        - **FSR (near lambda0)**: ~ **{fsr_nm:.2f} nm**
        - **Intrinsic Q estimate** from loss **{loss_db_per_cm_value:.1f} dB/cm**: **{qi_text}**

        Notes:
        - This is a *back-of-the-envelope* calculator: it ignores coupling details, dispersion beyond n_g,
          and any bend/coupler excess loss.
        - If you want a bigger FSR, reduce R; if you want a denser comb of resonances, increase R.
        """
    )
    return


@app.cell
def _(mo):
    import textwrap

    mo.md(
        textwrap.dedent(
            r"""
            ## Simphony example: an ideal all-pass ring

            This section builds a simple **all-pass ring resonator** using Simphony's `ideal` library
            (an ideal directional coupler + an ideal waveguide loop) and evaluates the **through-port**
            transmission versus wavelength.

            Notes:
            - The first time you run this in a fresh environment, imports can take a while (JAX init + many deps).
            - If you're working from a cloud-synced folder (Box/Dropbox/OneDrive), import time can be worse.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    coupling = mo.ui.slider(
        start=0.001,
        stop=0.3,
        step=0.001,
        value=0.05,
        label="Directional coupler power coupling (kappa)",
    )
    neff = mo.ui.slider(
        start=1.5,
        stop=3.5,
        step=0.01,
        value=2.34,
        label="Effective index n_eff (phase)",
    )
    span_nm = mo.ui.slider(
        start=1.0,
        stop=50.0,
        step=0.5,
        value=10.0,
        label="Spectrum span around lambda0 (nm)",
    )
    points = mo.ui.slider(
        start=200,
        stop=2000,
        step=100,
        value=800,
        label="Points",
    )
    mo.vstack([coupling, neff, span_nm, points])
    return coupling, neff, points, span_nm


@app.cell
def _(
    coupling,
    lambda0_nm,
    loss_db_per_cm,
    math,
    mo,
    neff,
    ng,
    points,
    radius_um,
    span_nm,
):
    simphony_error = ""
    S = None
    wl_um = None
    intensity = None
    import_seconds = None
    output = None

    try:  # pragma: no cover - depends on environment
        import time

        t0 = time.time()
        from jax import config

        config.update("jax_enable_x64", True)

        import jax.numpy as jnp
        import sax
        from simphony.libraries import ideal

        import_seconds = time.time() - t0

        _lambda0_um = float(lambda0_nm.value) * 1e-3
        _span_um = float(span_nm.value) * 1e-3
        wl_um = jnp.linspace(
            _lambda0_um - 0.5 * _span_um,
            _lambda0_um + 0.5 * _span_um,
            int(points.value),
        )

        _R_um = float(radius_um.value)
        _L_um = 2.0 * math.pi * _R_um

        ring_circuit, _ = sax.circuit(
            netlist={
                "instances": {
                    "dc": "coupler",
                    "loop": "waveguide",
                },
                "connections": {
                    # Close the ring loop between the two ring-side coupler ports.
                    "dc,o2": "loop,o0",
                    "loop,o1": "dc,o3",
                },
                "ports": {
                    "input": "dc,o0",
                    "through": "dc,o1",
                },
            },
            models={
                "coupler": ideal.coupler,
                "waveguide": ideal.waveguide,
            },
        )

        S = ring_circuit(
            wl=wl_um,
            dc={
                "coupling": float(coupling.value),
                "loss": 0.0,
                "phi": 0.5 * math.pi,
            },
            loop={
                "wl0": _lambda0_um,
                "neff": float(neff.value),
                "ng": float(ng.value),
                "length": _L_um,
                "loss": float(loss_db_per_cm.value),
            },
        )
        t_through = S["through", "input"]
        intensity = jnp.abs(t_through) ** 2
    except Exception as e:  # pragma: no cover
        simphony_error = f"{type(e).__name__}: {e}"

    if simphony_error:
        import sys

        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
        if (
            "No module named 'jax'" in simphony_error
            or 'No module named "jax"' in simphony_error
            or "No module named 'sax'" in simphony_error
            or 'No module named "sax"' in simphony_error
        ):
            output = mo.callout(
                mo.md(
                    (
                        "Simphony ring failed because required dependencies are missing.\n\n"
                        f"- Current Python: `{py_ver}`\n"
                        "- This Simphony example uses `simphony.libraries.ideal`, which imports `jax` and `sax`.\n\n"
                        "How to fix:\n"
                        "- **Recommended:** use marimo sandbox mode in a Python version with JAX wheels (often 3.11/3.12; Python 3.13 may not work):\n"
                        "  `marimo edit --sandbox marimo_course/lessons/w04_ring_resonators.py`\n"
                        "  (If your `marimo` is running under Python 3.13, use a 3.11/3.12 env, e.g. `./.venv/bin/python -m marimo ...`.)\n"
                        "- **Local venv:** install deps (may require Python 3.11/3.12):\n"
                        "  `./.venv/bin/pip install \"jax[cpu]\" sax`\n"
                    )
                ),
                kind="warn",
            )
        else:
            output = mo.md(f"Simphony ring failed: `{simphony_error}`")
    else:
        # Plot as a PNG for consistent rendering in marimo.
        import numpy as np
        from io import BytesIO

        import matplotlib.pyplot as plt

        wl_nm = np.array(wl_um) * 1e3
        y = np.array(intensity)

        fig, ax = plt.subplots(figsize=(6.5, 3.0))
        ax.plot(wl_nm, y, lw=1.5)
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel("Through transmission |S|^2")
        ax.set_title("Ideal all-pass ring (Simphony)")
        ax.grid(True, alpha=0.25)
        ax.set_ylim(-0.05, 1.05)

        subtitle = (
            f"R={float(radius_um.value):.1f} um, kappa={float(coupling.value):.2f}, "
            f"neff={float(neff.value):.2f}, ng={float(ng.value):.2f}, "
            f"loss={float(loss_db_per_cm.value):.2f} dB/cm"
        )
        ax.text(
            0.5,
            1.02,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=9,
        )

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        layout_buf = None
        layout_error = ""
        try:  # pragma: no cover - depends on local environment
            import gdsfactory as gf

            gf.gpdk.PDK.activate()

            c = gf.components.ring_single(
                radius=float(radius_um.value),
                gap=0.2,
                length_x=4.0,
            )
            fig_layout = c.plot(show_labels=False, show_ruler=False)
            if fig_layout is None:
                fig_layout = plt.gcf()

            layout_buf = BytesIO()
            fig_layout.savefig(layout_buf, format="png", bbox_inches="tight", dpi=150)
            plt.close(fig_layout)
            layout_buf.seek(0)
        except Exception as e:
            layout_error = f"{type(e).__name__}: {e}"
            layout_buf = None

        import_line = ""
        if import_seconds is not None:
            import_line = f"\n\nImport + init time: **{import_seconds:.1f} s**"

        layout_widget = None
        if layout_buf is not None:
            layout_widget = mo.image(layout_buf)
        elif layout_error:
            layout_widget = mo.callout(
                mo.md(
                    "Layout preview failed.\n\n"
                    f"- Error: `{layout_error}`\n\n"
                    "Tip: for sandbox mode, ensure `gdsfactory` can install in the sandbox environment."
                ),
                kind="warn",
            )

        blocks = [mo.image(buf)]
        if layout_widget is not None:
            blocks.append(mo.md("### Layout Preview (GDS)"))
            blocks.append(layout_widget)

        blocks.append(
            mo.md("Tip: decrease R for larger FSR; increase R for denser resonances." + import_line)
        )

        output = mo.vstack(blocks)

    output
    return


@app.cell
def _(mo):
    import textwrap as _textwrap

    mo.md(
        _textwrap.dedent(
            r"""
            ## Optional demo: MZI + ring resonator ("resonance-assisted interferometer")

            A plain MZI converts a **phase difference** between its arms into an **intensity** change at the outputs.
            If you embed a ring resonator in one arm, the ring adds a sharp, wavelength-dependent phase shift.

            The result is a compact, useful filter shape: near a ring resonance, the MZI output can show
            a sharp notch/peak (often a Fano-like lineshape) that you can tune with:
            - MZI coupler splitting ratio
            - ring coupling strength
            - MZI path-length imbalance (delta L)

            This is an "ideal" circuit model (no PDK specifics) but it demonstrates why rings are often paired
            with interferometers for sensing and filtering.
            """
        ).strip()
    )
    return


@app.cell
def _(mo):
    run_mzi_ring = mo.ui.checkbox(label="Run MZI + ring demo", value=False)
    mzi_kappa = mo.ui.slider(
        start=0.1,
        stop=0.9,
        step=0.01,
        value=0.5,
        label="MZI coupler power coupling (kappa)",
    )
    ring_kappa = mo.ui.slider(
        start=0.001,
        stop=0.3,
        step=0.001,
        value=0.03,
        label="Ring coupler power coupling (kappa)",
    )
    arm_length_um = mo.ui.slider(
        start=10.0,
        stop=5000.0,
        step=10.0,
        value=200.0,
        label="MZI nominal arm length (um)",
    )
    delta_L_um = mo.ui.slider(
        start=0.0,
        stop=2000.0,
        step=10.0,
        value=50.0,
        label="MZI path imbalance delta L (um)",
    )
    mo.vstack([run_mzi_ring, mzi_kappa, ring_kappa, arm_length_um, delta_L_um])
    return arm_length_um, delta_L_um, mzi_kappa, ring_kappa, run_mzi_ring


@app.cell
def _(
    arm_length_um,
    coupling,
    delta_L_um,
    lambda0_nm,
    loss_db_per_cm,
    math,
    mo,
    mzi_kappa,
    neff,
    ng,
    points,
    radius_um,
    ring_kappa,
    run_mzi_ring,
    span_nm,
):
    mo.stop(not bool(run_mzi_ring.value))

    demo_error = ""
    demo_output = None

    try:  # pragma: no cover - depends on environment
        from jax import config as _config

        _config.update("jax_enable_x64", True)

        import jax.numpy as _jnp
        import sax as _sax
        from simphony.libraries import ideal as _ideal

        _lambda0_um = float(lambda0_nm.value) * 1e-3
        _span_um = float(span_nm.value) * 1e-3
        _wl_um = _jnp.linspace(
            _lambda0_um - 0.5 * _span_um,
            _lambda0_um + 0.5 * _span_um,
            int(points.value),
        )

        _R_um = float(radius_um.value)
        _L_ring_um = 2.0 * math.pi * _R_um

        _L_arm_um = float(arm_length_um.value)
        _dL_um = float(delta_L_um.value)
        _L_a1 = 0.5 * _L_arm_um
        _L_a2 = 0.5 * _L_arm_um
        _L_b = _L_arm_um + _dL_um

        mzi_ring_circuit, _ = _sax.circuit(
            netlist={
                "instances": {
                    "dc1": "coupler",
                    "dc2": "coupler",
                    "arm_a1": "waveguide",
                    "arm_a2": "waveguide",
                    "arm_b": "waveguide",
                    "ring_dc": "coupler",
                    "ring_loop": "waveguide",
                },
                "connections": {
                    # Upper arm: dc1 -> arm_a1 -> ring coupler (through) -> arm_a2 -> dc2
                    "dc1,o1": "arm_a1,o0",
                    "arm_a1,o1": "ring_dc,o0",
                    "ring_dc,o1": "arm_a2,o0",
                    "arm_a2,o1": "dc2,o0",
                    # Lower arm: dc1 -> arm_b -> dc2
                    "dc1,o3": "arm_b,o0",
                    "arm_b,o1": "dc2,o2",
                    # Close the ring loop on the ring coupler.
                    "ring_dc,o2": "ring_loop,o0",
                    "ring_loop,o1": "ring_dc,o3",
                },
                "ports": {
                    "in": "dc1,o0",
                    "in2": "dc1,o2",
                    "out1": "dc2,o1",
                    "out2": "dc2,o3",
                },
            },
            models={
                "coupler": _ideal.coupler,
                "waveguide": _ideal.waveguide,
            },
        )

        _S = mzi_ring_circuit(
            wl=_wl_um,
            dc1={
                "coupling": float(mzi_kappa.value),
                "loss": 0.0,
                "phi": 0.5 * math.pi,
            },
            dc2={
                "coupling": float(mzi_kappa.value),
                "loss": 0.0,
                "phi": 0.5 * math.pi,
            },
            ring_dc={
                "coupling": float(ring_kappa.value),
                "loss": 0.0,
                "phi": 0.5 * math.pi,
            },
            ring_loop={
                "wl0": _lambda0_um,
                "neff": float(neff.value),
                "ng": float(ng.value),
                "length": _L_ring_um,
                "loss": float(loss_db_per_cm.value),
            },
            arm_a1={
                "wl0": _lambda0_um,
                "neff": float(neff.value),
                "ng": float(ng.value),
                "length": _L_a1,
                "loss": float(loss_db_per_cm.value),
            },
            arm_a2={
                "wl0": _lambda0_um,
                "neff": float(neff.value),
                "ng": float(ng.value),
                "length": _L_a2,
                "loss": float(loss_db_per_cm.value),
            },
            arm_b={
                "wl0": _lambda0_um,
                "neff": float(neff.value),
                "ng": float(ng.value),
                "length": _L_b,
                "loss": float(loss_db_per_cm.value),
            },
        )

        _t1 = _S["out1", "in"]
        _t2 = _S["out2", "in"]
        _y1 = _jnp.abs(_t1) ** 2
        _y2 = _jnp.abs(_t2) ** 2

        import numpy as _np
        from io import BytesIO as _BytesIO

        import matplotlib.pyplot as _plt

        _wl_nm = _np.array(_wl_um) * 1e3
        _y1_np = _np.array(_y1)
        _y2_np = _np.array(_y2)

        _fig, _ax = _plt.subplots(figsize=(6.5, 3.2))
        _ax.plot(_wl_nm, _y1_np, lw=1.6, label="out1")
        _ax.plot(_wl_nm, _y2_np, lw=1.6, label="out2", alpha=0.85)
        _ax.set_xlabel("Wavelength (nm)")
        _ax.set_ylabel("Transmission |S|^2")
        _ax.set_title("MZI + ring demo (Simphony ideal)")
        _ax.grid(True, alpha=0.25)
        _ax.set_ylim(-0.05, 1.05)
        _ax.legend(loc="best")

        _subtitle = (
            f"R={float(radius_um.value):.1f} um, ring kappa={float(ring_kappa.value):.3f}, "
            f"MZI kappa={float(mzi_kappa.value):.2f}, deltaL={float(delta_L_um.value):.0f} um"
        )
        _ax.text(
            0.5,
            1.02,
            _subtitle,
            transform=_ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=9,
        )

        _buf = _BytesIO()
        _fig.savefig(_buf, format="png", bbox_inches="tight")
        _plt.close(_fig)
        _buf.seek(0)

        _layout_buf = None
        _layout_error = ""
        try:  # pragma: no cover - depends on local environment
            import gdsfactory as _gf
            import uuid as _uuid

            _gf.gpdk.PDK.activate()

            _c = _gf.Component(f"mzi_plus_ring_demo_{_uuid.uuid4().hex[:8]}")
            # Use a 2x2 MZI so the layout has two outputs (matching the two outputs plotted above).
            _mzi = _gf.components.mzi2x2_2x2(
                delta_length=float(delta_L_um.value),
                add_optical_ports_arms=True,
            )
            _rmzi = _c << _mzi

            # Place a standalone ring (no bus waveguide) near the upper arm for a clean visual.
            _x4, _y4 = _rmzi.ports["o4"].center
            _x5, _y5 = _rmzi.ports["o5"].center
            _R = float(radius_um.value)
            _gap = 0.2
            _ring_ref = _c << _gf.components.ring(radius=_R)
            _xmid = 0.5 * float(_x4 + _x5)
            _ymid = float(_y4 + _y5) * 0.5
            _ring_ref.move((_xmid, _ymid + _R + _gap + 0.5))

            _layout_fig = _c.plot(show_labels=True, show_ruler=False)
            if _layout_fig is None:
                _layout_fig = _plt.gcf()

            _layout_buf = _BytesIO()
            _layout_fig.savefig(_layout_buf, format="png", bbox_inches="tight", dpi=150)
            _plt.close(_layout_fig)
            _layout_buf.seek(0)
        except Exception as e:
            _layout_error = f"{type(e).__name__}: {e}"
            _layout_buf = None

        _layout_widget = None
        if _layout_buf is not None:
            _layout_widget = mo.image(_layout_buf)
        elif _layout_error:
            _layout_widget = mo.callout(
                mo.md(
                    "Layout preview failed.\n\n"
                    f"- Error: `{_layout_error}`\n\n"
                    "Tip: for sandbox mode, ensure `gdsfactory` can install in the sandbox environment."
                ),
                kind="warn",
            )

        _blocks = [mo.image(_buf)]
        if _layout_widget is not None:
            _blocks.append(mo.md("### Layout Preview (GDS)"))
            _blocks.append(_layout_widget)

        _blocks.append(
            mo.md(
                "Try: set `MZI kappa` near 0.5, then sweep `ring kappa` and `delta L` to shape the notch/peak."
            )
        )

        demo_output = mo.vstack(_blocks)
    except Exception as e:  # pragma: no cover
        demo_error = f"{type(e).__name__}: {e}"

    if demo_error:
        demo_output = mo.callout(mo.md(f"MZI + ring demo failed: `{demo_error}`"), kind="warn")

    demo_output
    return


if __name__ == "__main__":
    app.run()
