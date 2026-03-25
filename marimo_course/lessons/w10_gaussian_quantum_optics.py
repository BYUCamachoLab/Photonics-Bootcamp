#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.18.4",
#   "simphony==0.7.3",
#   "matplotlib",
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
        options=("All", "Overview", "Theory", "Interactive", "Entanglement", "Application", "Exercises"),
        value="All",
        label="Notebook sections",
    )
    section_tabs
    return set_view, view_state


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_theory = view in ["All", "Theory"]
    show_interactive = view in ["All", "Interactive"]
    show_entanglement = view in ["All", "Entanglement"]
    show_application = view in ["All", "Application"]
    show_exercises = view in ["All", "Exercises"]
    return show_application, show_entanglement, show_exercises, show_interactive, show_overview, show_theory, view


@app.cell
def _(doc_badges, show_application, show_entanglement, show_exercises, show_interactive, show_overview, show_theory, view):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
            (
                "Flags: "
                f"overview={show_overview}, "
                f"theory={show_theory}, "
                f"interactive={show_interactive}, "
                f"entanglement={show_entanglement}, "
                f"application={show_application}, "
                f"exercises={show_exercises}"
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
        title="Gaussian quantum optics with Simphony",
        subtitle=(
            "A first look at how Gaussian quantum states move through linear photonic circuits, "
            "with a direct comparison to the classical simulations you already know."
        ),
        badges=[
            "Week 10",
            "Quantum optics",
            "Simphony",
            "Gaussian states",
            "Linear circuits",
            "Intro lesson",
        ],
        toc=[
            ("Overview", "overview"),
            ("Why quantum here?", "why-quantum"),
            ("Glossary", "glossary"),
            ("Theory", "theory"),
            ("Phase-space view", "phase-space-view"),
            ("Interactive studio", "interactive"),
            ("Entanglement preview", "entanglement"),
            ("Useful circuit example", "application"),
            ("Exercises", "exercises"),
        ],
        build="2026-03-23",
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
        restore_command="git -C Photonics-Bootcamp restore marimo_course/lessons/w10_gaussian_quantum_optics.py",
        external_check_command="python3 marimo_course/lessons/check_notebook_health.py marimo_course/lessons/w10_gaussian_quantum_optics.py",
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
    doc_callout_list(
        "info",
        tag="Roadmap",
        title="What this lesson does",
        ordered=True,
        items=[
            "<strong>Connect to prior knowledge:</strong> start from the classical scattering picture you already know.",
            "<strong>First new idea:</strong> add single-mode uncertainty through variances in the X and P quadratures.",
            "<strong>Use Simphony hands-on:</strong> create coherent, squeezed, and thermal states and send them through a coupler or MZI.",
            "<strong>Second new idea:</strong> after the variance picture is clear, introduce covariance between modes and preview entanglement.",
        ],
    )

    doc_callout_list(
        "warning",
        tag="Scope",
        title="What this notebook is and is not",
        items=[
            "This is <strong>not</strong> a full quantum mechanics lesson and it is <strong>not</strong> a single-photon or qubit lesson.",
            "We stay inside <strong>Gaussian quantum optics</strong>.",
            "For most of this notebook, you only need to think about a mean field plus <strong>variance</strong> in each quadrature.",
            "The main goal is to understand how a <strong>linear photonic circuit</strong> can be simulated in both classical and quantum ways.",
        ],
    )
    return


@app.cell
def _(doc_callout_html, mo, show_overview):
    mo.stop(not show_overview)
    mo.md(
        r"""
        <a id="overview"></a>
        ## Lesson goals

        By the end of this notebook, you should be able to:

        - explain the difference between a classical field simulation and a Gaussian quantum simulation,
        - create a few standard Gaussian states in Simphony,
        - propagate those states through a linear photonic circuit, and
        - interpret the output in terms of both <strong>mean field</strong> and <strong>uncertainty</strong>.
        """
    )
    doc_callout_html(
        "info",
        tag="Key idea",
        title="One sentence to remember",
        html=(
            "<p>"
            "A <strong>coherent state</strong> in a linear photonic circuit follows the same mean-field transfer "
            "law as the classical simulation, but the quantum simulation also keeps track of "
            "<strong>uncertainty and noise</strong> through the quadrature variances."
            "</p>"
        ),
    )
    return


@app.cell
def _(mo, set_view, show_overview):
    mo.stop(not show_overview)
    go_interactive = mo.ui.button(
        value=0,
        kind="success",
        label="Go to Interactive studio",
        on_click=lambda v: (set_view("Interactive"), (v or 0) + 1)[-1],
    )
    go_application = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to sensing example",
        on_click=lambda v: (set_view("Application"), (v or 0) + 1)[-1],
    )
    go_entanglement = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to entanglement preview",
        on_click=lambda v: (set_view("Entanglement"), (v or 0) + 1)[-1],
    )
    mo.hstack([go_interactive, go_application, go_entanglement], justify="start", gap=1.0)
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    mo.md(
        r"""
        <a id="glossary"></a>
        ## Quick glossary

        - **Mode**: one optical degree of freedom, usually attached to a named circuit port.
        - **Quadratures `X` and `P`**: the two real coordinates used to describe a Gaussian optical state.
        - **Mean field**: the average phasor-like location of the state in the `X-P` plane.
        - **Variance**: how wide the uncertainty is in one quadrature direction.
        - **Covariance**: how strongly two coordinates move together; in this lesson it matters mainly when comparing two modes.
        - **Squeezing**: reducing uncertainty in one quadrature while increasing it in the other.
        """
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    mo.md(
        r"""
        <a id="why-quantum"></a>
        ## Why bother with a quantum simulation if we already have a classical one?

        In the classical picture, a circuit takes an input field amplitude vector $a_{\mathrm{in}}$ and returns
        an output field amplitude vector

        $$
        a_{\mathrm{out}} = S a_{\mathrm{in}},
        $$

        where $S$ is the scattering matrix of the circuit.

        That is enough if your main question is:

        - “What fraction of the optical power leaves each port?”
        - “How does the response change with wavelength?”
        - “What phase does each path accumulate?”

        In a Gaussian quantum simulation, we ask a slightly richer question:

        - “What happens to both the <strong>average field</strong> and the <strong>uncertainty</strong> of the state?”

        So the quantum simulation does not replace the classical one. It extends it.
        """
    )
    return


@app.cell
def _(doc_callout_html, mo, show_theory):
    mo.stop(not show_theory)
    mo.md(
        r"""
        <a id="theory"></a>
        ## Minimal theory: just enough to use the tool

        We only need three ideas, and we will learn them in order.

        ### 1. A mode has two quadratures

        For each optical mode, Simphony tracks two real-valued coordinates:

        - $X$ quadrature
        - $P$ quadrature

        You can think of these as phase-space coordinates. For a single mode, we will track:

        - a 2-element mean vector, and
        - the spread of the state in the X and P directions.

        ### 2. First focus on mean + variance

        Before talking about correlations between different modes, first get comfortable with:

        - where the phasor-like mean sits in the X-P plane, and
        - how wide the uncertainty is in X and P.

        In this lesson we use three standard examples:

        - <strong>Coherent state:</strong> displaced vacuum, circular uncertainty.
        - <strong>Squeezed state:</strong> one quadrature uncertainty gets smaller while the other gets larger.
        - <strong>Thermal state:</strong> centered at zero mean but with larger, isotropic noise.

        ### 3. Linear circuits act on the mean and the uncertainty

        A passive linear photonic circuit transforms:

        $$
        \mu_{\mathrm{out}} = T \mu_{\mathrm{in}}, \qquad
        \Sigma_{\mathrm{out}} = T \Sigma_{\mathrm{in}} T^T,
        $$

        where $\mu$ is the mean vector, $\Sigma$ is the uncertainty matrix, and $T$ is the quadrature-space
        transform built from the circuit scattering matrix.
        """
    )
    doc_callout_html(
        "info",
        tag="Comparison",
        title="Classical vs Gaussian quantum simulation",
        html=r"""
        <table>
          <thead>
            <tr>
              <th>Question</th>
              <th>Classical simulation</th>
              <th>Gaussian quantum simulation</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>What is the state?</td>
              <td>Complex field amplitudes</td>
              <td>Quadrature means + variances</td>
            </tr>
            <tr>
              <td>What is propagated?</td>
              <td>Amplitude vector through <code>S</code></td>
              <td>Means and uncertainty through a quadrature transform</td>
            </tr>
            <tr>
              <td>What does loss do?</td>
              <td>Reduces output amplitude/power</td>
              <td>Couples in vacuum modes and changes uncertainty</td>
            </tr>
            <tr>
              <td>What extra information do we get?</td>
              <td>Power and phase response</td>
              <td>Noise ellipse, squeezing, thermal broadening</td>
            </tr>
          </tbody>
        </table>
        """,
    )
    return


@app.cell
def _(doc_callout_html, mo, show_theory):
    mo.stop(not show_theory)
    doc_callout_html(
        "info",
        tag="Mental model",
        title="The picture to keep in mind",
        html=(
            "<p>"
            "Start with the classical phasor you already know. Then add a fuzzy cloud around it. "
            "For most of this notebook, that cloud is summarized by two numbers: `Var(X)` and `Var(P)`."
            "</p>"
        ),
    )
    return


@app.cell
def _(doc_callout_html, mo, plot_phase_space_progression, show_theory):
    mo.stop(not show_theory)
    mo.md(
        r"""
        <a id="phase-space-view"></a>
        ## Phase-space picture: point to blob to squeezed ellipse

        This is the visual progression to keep in mind throughout the notebook:

        - A **classical phasor** is just a point or arrow in phase space.
        - A **Gaussian quantum state** keeps that same mean location, but now adds a spread around it.
        - A **squeezed state** keeps the Gaussian shape, but stretches it in one direction and compresses it in the other.

        In the figure below, the mean field is the same in every panel. Only the uncertainty changes.
        """
    )
    doc_callout_html(
        "info",
        tag="How to read this",
        title="What squeezing looks like",
        html=(
            "<p>The arrow tip marks the mean field.</p>"
            "<p>The blue cloud shows where the state is spread in phase space.</p>"
            "<p>A circular cloud means similar uncertainty in <code>X</code> and <code>P</code>. "
            "An ellipse means the uncertainty is direction-dependent.</p>"
            "<p>Changing the squeeze angle rotates that ellipse without moving the mean.</p>"
        ),
    )
    plot_phase_space_progression()
    return


@app.cell
def _(mo, show_theory):
    mo.stop(not show_theory)
    mo.md(
        r"""
        ## How Simphony represents this

        In the installed version used by this course (`simphony==0.7.3`), the relevant classes are:

        - `CoherentState`
        - `SqueezedState`
        - `ThermalState`
        - `QuantumState`
        - `QuantumSim`
        - `compose_qstate`

        `QuantumSim` takes the same kind of circuit model used in the classical workflow and extends it to a
        Gaussian quantum simulation. This is useful pedagogically because the <strong>circuit stays familiar</strong>
        even though the notion of “state” changes.
        """
    )
    return


@app.cell
def _():
    import math

    return (math,)


@app.cell
def _(math):
    import matplotlib.pyplot as plt
    import numpy as np
    from jax import config

    config.update("jax_enable_x64", True)

    import jax.numpy as jnp
    import sax
    from sax.utils import get_ports
    from simphony.libraries import ideal
    from simphony.quantum import (
        CoherentState,
        QuantumSim,
        SqueezedState,
        ThermalState,
        TwoModeSqueezedState,
        compose_qstate,
    )

    def build_coupler_circuit():
        return sax.circuit(
            netlist={
                "instances": {
                    "dc": "coupler",
                },
                "connections": {},
                "ports": {
                    "in0": "dc,o0",
                    "out0": "dc,o1",
                    "in1": "dc,o2",
                    "out1": "dc,o3",
                },
            },
            models={"coupler": ideal.coupler},
        )[0]

    def build_mzi_circuit():
        return sax.circuit(
            netlist={
                "instances": {
                    "dc_in": "coupler",
                    "top": "waveguide",
                    "bottom": "waveguide",
                    "dc_out": "coupler",
                },
                "connections": {
                    "dc_in,o1": "top,o0",
                    "dc_in,o3": "bottom,o0",
                    "top,o1": "dc_out,o1",
                    "bottom,o1": "dc_out,o3",
                },
                "ports": {
                    "in0": "dc_in,o0",
                    "in1": "dc_in,o2",
                    "out0": "dc_out,o0",
                    "out1": "dc_out,o2",
                },
            },
            models={
                "coupler": ideal.coupler,
                "waveguide": ideal.waveguide,
            },
        )[0]

    def make_input_state(state_kind, alpha_x, alpha_p, squeeze_r, squeeze_phi_deg, thermal_nbar):
        alpha = complex(alpha_x, alpha_p)
        if state_kind == "Coherent":
            return CoherentState("in0", alpha)
        if state_kind == "Squeezed":
            return SqueezedState(
                "in0",
                r=squeeze_r,
                phi=np.deg2rad(squeeze_phi_deg),
                alpha=alpha,
            )
        return ThermalState("in0", nbar=thermal_nbar)

    def vacuum_state(port):
        return CoherentState(port, 0.0 + 0.0j)

    def alpha_from_mode_means(means):
        return complex(float(means[0]), float(means[1]))

    def photon_number_from_state(mode_means, mode_cov):
        x_mean = float(mode_means[0])
        p_mean = float(mode_means[1])
        x_var = float(mode_cov[0, 0])
        p_var = float(mode_cov[1, 1])
        return x_mean**2 + p_mean**2 + x_var + p_var - 0.5

    def format_array(values, digits=3):
        arr = np.asarray(values, dtype=float)
        return np.array2string(arr, precision=digits, suppress_small=True)

    def plot_single_mode(qstate, mode, title):
        means, cov = qstate.modes(mode)
        fig, ax = plt.subplots(figsize=(4.0, 4.0))
        qstate.plot_mode(mode, n=140, ax=ax, cmap="Blues")
        ax.set_title(title)
        fig.tight_layout()
        return fig, means, cov

    def plot_phasor_with_uncertainty(means, cov, title):
        from matplotlib.patches import Ellipse

        means = np.asarray(means, dtype=float)
        cov = np.asarray(cov, dtype=float)

        evals, evecs = np.linalg.eigh(cov)
        order = np.argsort(evals)[::-1]
        evals = evals[order]
        evecs = evecs[:, order]
        angle_deg = np.degrees(np.arctan2(evecs[1, 0], evecs[0, 0]))

        fig, ax = plt.subplots(figsize=(4.4, 4.4))
        x, p = means
        spread = max(np.sqrt(max(evals[-1], 0.0)) * 4.0, 1.0)
        radius = max(np.sqrt(x**2 + p**2) * 1.25, spread)

        ax.axhline(0.0, color="0.75", lw=1)
        ax.axvline(0.0, color="0.75", lw=1)
        ax.quiver(
            0.0,
            0.0,
            x,
            p,
            angles="xy",
            scale_units="xy",
            scale=1,
            color="#2563eb",
            width=0.012,
        )

        ellipse = Ellipse(
            xy=(x, p),
            width=4.0 * np.sqrt(max(evals[0], 0.0)),
            height=4.0 * np.sqrt(max(evals[1], 0.0)),
            angle=angle_deg,
            facecolor="#93c5fd",
            edgecolor="#1d4ed8",
            alpha=0.45,
            lw=2,
        )
        ax.add_patch(ellipse)
        ax.scatter([x], [p], color="#1d4ed8", s=35, zorder=3)

        ax.set_xlim(-radius, radius)
        ax.set_ylim(-radius, radius)
        ax.set_aspect("equal")
        ax.set_xlabel("X quadrature")
        ax.set_ylabel("P quadrature")
        ax.set_title(title)
        fig.tight_layout()
        return fig

    def plot_phase_space_progression():
        from matplotlib.patches import Ellipse

        def _gaussian_density(mean, cov, x_grid, p_grid):
            mean = np.asarray(mean, dtype=float)
            cov = np.asarray(cov, dtype=float)
            cov = cov + 1e-12 * np.eye(2)
            inv_cov = np.linalg.inv(cov)
            det_cov = np.linalg.det(cov)
            dx = x_grid - mean[0]
            dp = p_grid - mean[1]
            quad = (
                inv_cov[0, 0] * dx**2
                + 2.0 * inv_cov[0, 1] * dx * dp
                + inv_cov[1, 1] * dp**2
            )
            return np.exp(-0.5 * quad) / (2.0 * np.pi * np.sqrt(det_cov))

        def _squeezed_covariance(r, phi_deg):
            phi = np.deg2rad(phi_deg)
            rot = np.array(
                [
                    [np.cos(phi), -np.sin(phi)],
                    [np.sin(phi), np.cos(phi)],
                ]
            )
            base = 0.25 * np.diag([np.exp(-2.0 * r), np.exp(2.0 * r)])
            return rot @ base @ rot.T

        def _add_uncertainty_ellipse(ax, mean, cov):
            evals, evecs = np.linalg.eigh(cov)
            order = np.argsort(evals)[::-1]
            evals = evals[order]
            evecs = evecs[:, order]
            angle_deg = np.degrees(np.arctan2(evecs[1, 0], evecs[0, 0]))
            ellipse = Ellipse(
                xy=mean,
                width=4.0 * np.sqrt(max(evals[0], 0.0)),
                height=4.0 * np.sqrt(max(evals[1], 0.0)),
                angle=angle_deg,
                fill=False,
                edgecolor="#1d4ed8",
                lw=2,
            )
            ax.add_patch(ellipse)

        mean = np.array([1.2, 0.6], dtype=float)
        coherent_cov = 0.25 * np.eye(2)
        squeezed_x_cov = _squeezed_covariance(0.9, 0.0)
        squeezed_rot_cov = _squeezed_covariance(0.9, 35.0)

        x = np.linspace(-2.5, 2.5, 220)
        p = np.linspace(-2.5, 2.5, 220)
        xx, pp = np.meshgrid(x, p)

        panels = [
            ("Classical point", None, "#dc2626"),
            ("Quantum Gaussian", coherent_cov, "#2563eb"),
            ("X-squeezed", squeezed_x_cov, "#2563eb"),
            ("Rotated squeeze", squeezed_rot_cov, "#2563eb"),
        ]

        fig, axes = plt.subplots(1, 4, figsize=(13.0, 3.4))
        for ax, (title, cov, point_color) in zip(axes, panels):
            ax.axhline(0.0, color="0.82", lw=1)
            ax.axvline(0.0, color="0.82", lw=1)
            ax.quiver(
                0.0,
                0.0,
                mean[0],
                mean[1],
                angles="xy",
                scale_units="xy",
                scale=1,
                color=point_color,
                width=0.012,
            )
            ax.scatter([mean[0]], [mean[1]], color=point_color, s=34, zorder=3)

            if cov is not None:
                density = _gaussian_density(mean, cov, xx, pp)
                ax.contourf(xx, pp, density, levels=8, cmap="Blues", alpha=0.9)
                _add_uncertainty_ellipse(ax, mean, cov)

            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.set_aspect("equal")
            ax.set_title(title, fontsize=10)
            ax.set_xlabel("X")
            if ax is axes[0]:
                ax.set_ylabel("P")

        fig.suptitle("Same mean field, different phase-space pictures", y=1.02, fontsize=13)
        fig.tight_layout()
        return fig

    def plot_covariance_matrix(output_state, physical_ports, include_loss_modes, title):
        cov = np.asarray(output_state.cov, dtype=float)
        if include_loss_modes:
            n_modes = output_state.N
            labels = list(physical_ports) + [
                f"loss_{idx}" for idx in range(output_state.N - len(physical_ports))
            ]
        else:
            n_modes = len(physical_ports)
            labels = list(physical_ports)

        cov = cov[: 2 * n_modes, : 2 * n_modes]
        quad_labels = [f"{label}:X" for label in labels] + [f"{label}:P" for label in labels]

        fig, ax = plt.subplots(figsize=(6.0, 5.2))
        im = ax.imshow(cov, cmap="RdBu_r")
        ax.set_title(title)
        ax.set_xticks(np.arange(len(quad_labels)))
        ax.set_yticks(np.arange(len(quad_labels)))
        ax.set_xticklabels(quad_labels, rotation=90, fontsize=8)
        ax.set_yticklabels(quad_labels, fontsize=8)
        fig.colorbar(im, ax=ax, shrink=0.85, label="Covariance")
        fig.tight_layout()
        return fig

    def build_quantum_summary_md(input_state, output_state, physical_ports):
        lines = []
        lines.append("### State summary")
        lines.append("")
        lines.append(f"- Input ports explicitly initialized: `{input_state.ports}`")
        lines.append(
            "- All uninitialized ports are treated as vacuum when `QuantumSim` builds the full multimode state."
        )
        lines.append(f"- Physical circuit ports: `{physical_ports}`")
        lines.append(f"- Total simulated modes in the output state: `{output_state.N}`")
        return "\n".join(lines)

    def build_active_controls_md(state_kind, circuit_kind):
        state_lines = {
            "Coherent": [
                "`Re(alpha)` and `Im(alpha)` matter most.",
                "`r`, `phi`, and `nbar` are ignored for this state choice.",
            ],
            "Squeezed": [
                "`Re(alpha)` and `Im(alpha)` set the displacement of the squeezed state.",
                "`r` controls the squeeze strength and `phi` rotates the squeeze axis.",
                "`nbar` is ignored for this state choice.",
            ],
            "Thermal": [
                "`nbar` controls the width of the thermal state.",
                "`Re(alpha)`, `Im(alpha)`, `r`, and `phi` are ignored for this state choice.",
            ],
        }
        circuit_lines = {
            "Coupler": [
                "`coupling` and component loss matter here.",
                "`DeltaL` does not affect the coupler case.",
            ],
            "MZI": [
                "`DeltaL` shifts the interferometer phase and spectral fringes.",
                "`coupling` still controls the splitter/combiner behavior.",
            ],
        }
        lines = ["### Active controls", ""] + [f"- {line}" for line in state_lines[state_kind]]
        lines += [f"- {line}" for line in circuit_lines[circuit_kind]]
        return "\n".join(lines)

    def build_guided_observation_md(state_kind, circuit_kind, selected_label, x_var, p_var):
        lines = ["### What to look for right now", ""]
        if state_kind == "Coherent":
            lines.append(
                "- Coherent-state means should track the same transfer trend as the classical field amplitudes."
            )
            lines.append(
                "- The uncertainty should stay close to a vacuum-like circular footprint unless loss or mixing changes the mode basis."
            )
        elif state_kind == "Squeezed":
            lines.append(
                "- Focus on the imbalance between `Var(X)` and `Var(P)`: that is the visible signature of squeezing."
            )
            lines.append(
                "- The mean may look ordinary while the variance carries the most important new physics."
            )
        else:
            lines.append(
                "- A thermal state usually stays centered near zero mean while keeping large isotropic uncertainty."
            )
            lines.append(
                "- This is the cleanest example of a state where noise dominates over displacement."
            )

        if circuit_kind == "MZI":
            lines.append(
                "- In the MZI case, compare how the classical transmission fringes line up with changes in the selected mode variances."
            )
        else:
            lines.append(
                "- In the coupler case, use the 50/50 split intuition to predict where the mean field should go."
            )

        lines.append(
            f"- For the currently selected mode `{selected_label}`, compare `Var(X) = {x_var:.3f}` and `Var(P) = {p_var:.3f}`."
        )
        return "\n".join(lines)

    def build_phasor_bridge_md():
        return "\n".join(
            [
                "### Phasor bridge",
                "",
                "- In your circuits and electromagnetics classes, a phasor is a point or arrow in the complex plane.",
                "- In this notebook, the mean vector `(X, P)` plays that same role: it is the quantum version of the average phasor.",
                "- The new ingredient is the ellipse around the tip of the phasor. That ellipse is the uncertainty.",
                "- A coherent state looks like a phasor with a roughly circular uncertainty cloud.",
                "- A squeezed state keeps the phasor idea, but the uncertainty becomes directional.",
            ]
        )

    def build_entanglement_intro_md():
        return "\n".join(
            [
                "### Entanglement preview",
                "",
                "- A single-mode uncertainty ellipse is not yet entanglement.",
                "- Entanglement shows up when two modes share correlations that cannot be described as two independent states.",
                "- In a Gaussian model, those correlations live in the off-diagonal blocks of the covariance matrix.",
                "- The simplest preview is a `TwoModeSqueezedState`: each mode alone can look noisy, but together they share structured covariance.",
            ]
        )

    def build_two_mode_product_state(r):
        return compose_qstate(
            SqueezedState("in0", r=r, phi=0.0, alpha=0.0),
            SqueezedState("in1", r=r, phi=0.0, alpha=0.0),
        )

    def build_two_mode_entangled_state(r, thermal_n):
        return TwoModeSqueezedState(
            r=r,
            n_a=thermal_n,
            n_b=thermal_n,
            port_a="in0",
            port_b="in1",
        )

    def covariance_correlation_summary(qstate):
        qstate.to_xpxp()
        means0, cov0 = qstate.modes(0)
        means1, cov1 = qstate.modes(1)
        cov = np.asarray(qstate.cov, dtype=float)
        x0x1 = float(cov[0, 2])
        p0p1 = float(cov[1, 3])
        return {
            "x0x1": x0x1,
            "p0p1": p0p1,
            "var_x0": float(cov0[0, 0]),
            "var_p0": float(cov0[1, 1]),
            "var_x1": float(cov1[0, 0]),
            "var_p1": float(cov1[1, 1]),
        }

    return (
        CoherentState,
        QuantumSim,
        TwoModeSqueezedState,
        alpha_from_mode_means,
        build_active_controls_md,
        build_coupler_circuit,
        build_entanglement_intro_md,
        build_guided_observation_md,
        build_phasor_bridge_md,
        build_mzi_circuit,
        build_quantum_summary_md,
        build_two_mode_entangled_state,
        build_two_mode_product_state,
        compose_qstate,
        covariance_correlation_summary,
        format_array,
        get_ports,
        jnp,
        make_input_state,
        math,
        np,
        photon_number_from_state,
        plot_covariance_matrix,
        plot_phase_space_progression,
        plot_phasor_with_uncertainty,
        plot_single_mode,
        plt,
        vacuum_state,
    )


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    state_kind = mo.ui.radio(
        options=["Coherent", "Squeezed", "Thermal"],
        value="Coherent",
        label="Input state",
        inline=True,
    )
    circuit_kind = mo.ui.radio(
        options=["Coupler", "MZI"],
        value="Coupler",
        label="Circuit",
        inline=True,
    )
    mo.hstack([state_kind, circuit_kind], justify="start", gap=1.5)
    return circuit_kind, state_kind


@app.cell
def _(mo, show_interactive, state_kind):
    mo.stop(not show_interactive)
    alpha_x = mo.ui.slider(
        start=-2.0,
        stop=2.0,
        step=0.1,
        value=1.0,
        label="Displacement X = Re(alpha)",
    )
    alpha_p = mo.ui.slider(
        start=-2.0,
        stop=2.0,
        step=0.1,
        value=0.0,
        label="Displacement P = Im(alpha)",
    )
    squeeze_r = mo.ui.slider(
        start=0.0,
        stop=1.4,
        step=0.05,
        value=0.6,
        label="Squeezing strength r",
    )
    squeeze_phi_deg = mo.ui.slider(
        start=0.0,
        stop=180.0,
        step=5.0,
        value=0.0,
        label="Squeezing angle phi (deg)",
    )
    thermal_nbar = mo.ui.slider(
        start=0.0,
        stop=4.0,
        step=0.1,
        value=1.0,
        label="Thermal occupation nbar",
    )
    state_controls = mo.vstack(
        [
            alpha_x,
            alpha_p,
            squeeze_r,
            squeeze_phi_deg,
            thermal_nbar,
        ]
    )
    mo.accordion(
        {
            f"State controls ({state_kind.value})": state_controls,
        }
    )
    return alpha_p, alpha_x, squeeze_phi_deg, squeeze_r, thermal_nbar


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    coupling = mo.ui.slider(
        start=0.05,
        stop=0.95,
        step=0.05,
        value=0.5,
        label="Coupler power coupling",
    )
    component_loss_db = mo.ui.slider(
        start=0.0,
        stop=3.0,
        step=0.1,
        value=0.0,
        label="Coupler/component loss (dB)",
    )
    delta_l_um = mo.ui.slider(
        start=0.0,
        stop=200.0,
        step=5.0,
        value=80.0,
        label="MZI extra path length DeltaL (um)",
    )
    wl0_nm = mo.ui.slider(
        start=1540.0,
        stop=1560.0,
        step=0.5,
        value=1550.0,
        label="Center wavelength (nm)",
    )
    span_nm = mo.ui.slider(
        start=2.0,
        stop=40.0,
        step=1.0,
        value=12.0,
        label="Sweep span (nm)",
    )
    n_points = mo.ui.slider(
        start=31,
        stop=201,
        step=10,
        value=81,
        label="Number of wavelength points",
    )
    selected_mode = mo.ui.slider(
        start=0,
        stop=7,
        step=1,
        value=0,
        label="Mode index to inspect",
    )
    wl_index = mo.ui.slider(
        start=0,
        stop=80,
        step=1,
        value=40,
        label="Wavelength index to inspect",
    )
    include_loss_modes = mo.ui.checkbox(
        label="Include loss modes in summary plots",
        value=False,
    )
    mo.accordion(
        {
            "Circuit and simulation controls": mo.vstack(
                [
                    coupling,
                    component_loss_db,
                    delta_l_um,
                    wl0_nm,
                    span_nm,
                    n_points,
                    include_loss_modes,
                    wl_index,
                    selected_mode,
                ]
            )
        }
    )
    return (
        component_loss_db,
        coupling,
        delta_l_um,
        include_loss_modes,
        n_points,
        selected_mode,
        span_nm,
        wl0_nm,
        wl_index,
    )


@app.cell
def _(
    alpha_x,
    alpha_p,
    build_active_controls_md,
    build_coupler_circuit,
    build_guided_observation_md,
    build_phasor_bridge_md,
    build_mzi_circuit,
    build_quantum_summary_md,
    circuit_kind,
    component_loss_db,
    compose_qstate,
    coupling,
    delta_l_um,
    format_array,
    get_ports,
    jnp,
    make_input_state,
    n_points,
    np,
    photon_number_from_state,
    plot_covariance_matrix,
    plot_phasor_with_uncertainty,
    selected_mode,
    span_nm,
    state_kind,
    thermal_nbar,
    vacuum_state,
    wl0_nm,
    wl_index,
    squeeze_phi_deg,
    squeeze_r,
):
    input_state = make_input_state(
        state_kind.value,
        alpha_x.value,
        alpha_p.value,
        squeeze_r.value,
        squeeze_phi_deg.value,
        thermal_nbar.value,
    )
    qstate_in = compose_qstate(input_state, vacuum_state("in1"))

    wl_um = jnp.linspace(
        (wl0_nm.value - 0.5 * span_nm.value) * 1e-3,
        (wl0_nm.value + 0.5 * span_nm.value) * 1e-3,
        int(n_points.value),
    )
    if circuit_kind.value == "Coupler":
        circuit = build_coupler_circuit()
        sim = QuantumSim(
            circuit,
            wl=wl_um,
            dc={
                "coupling": float(coupling.value),
                "loss": float(component_loss_db.value),
                "phi": 0.5 * np.pi,
            },
        )
        circuit_details = {
            "dc": {
                "coupling": float(coupling.value),
                "loss": float(component_loss_db.value),
                "phi": 0.5 * np.pi,
            }
        }
    else:
        circuit = build_mzi_circuit()
        base_length_um = 200.0
        sim = QuantumSim(
            circuit,
            wl=wl_um,
            dc_in={
                "coupling": float(coupling.value),
                "loss": float(component_loss_db.value),
                "phi": 0.5 * np.pi,
            },
            dc_out={
                "coupling": float(coupling.value),
                "loss": float(component_loss_db.value),
                "phi": 0.5 * np.pi,
            },
            top={
                "wl0": wl0_nm.value * 1e-3,
                "neff": 2.34,
                "ng": 3.40,
                "length": base_length_um + float(delta_l_um.value),
                "loss": 0.0,
            },
            bottom={
                "wl0": wl0_nm.value * 1e-3,
                "neff": 2.34,
                "ng": 3.40,
                "length": base_length_um,
                "loss": 0.0,
            },
        )
        circuit_details = {
            "coupling": float(coupling.value),
            "loss_dB_per_component": float(component_loss_db.value),
            "delta_l_um": float(delta_l_um.value),
        }

    sim.add_qstate(qstate_in)
    result = sim.run()

    physical_ports = list(get_ports(circuit()))
    safe_wl_index = min(int(wl_index.value), len(result.wl) - 1)
    output_state = result.state(wl_ind=safe_wl_index)
    output_state.to_xpxp()
    n_total_modes = output_state.N

    mode_index = min(int(selected_mode.value), n_total_modes - 1)
    means_mode, cov_mode = output_state.modes(mode_index)
    x_var = float(cov_mode[0, 0])
    p_var = float(cov_mode[1, 1])
    nbar_mode = photon_number_from_state(means_mode, cov_mode)
    selected_mode_label = (
        physical_ports[mode_index]
        if mode_index < len(physical_ports)
        else f"loss_mode_{mode_index - len(physical_ports)}"
    )
    selected_mode_kind = "physical port" if mode_index < len(physical_ports) else "loss mode"

    classical_port_names = physical_ports
    s_wl = np.asarray(result.s_params[safe_wl_index])
    classical_input = np.zeros(len(classical_port_names), dtype=complex)
    if "in0" in classical_port_names:
        classical_input[classical_port_names.index("in0")] = complex(
            alpha_x.value, alpha_p.value
        )
    classical_output = s_wl @ classical_input
    classical_power = np.abs(classical_output) ** 2

    mode_rows = []
    for _port_idx, _port_name in enumerate(physical_ports):
        port_means, port_cov = output_state.modes(_port_idx)
        mode_rows.append(
            {
                "port": _port_name,
                "alpha_classical_real": float(classical_output[_port_idx].real),
                "alpha_classical_imag": float(classical_output[_port_idx].imag),
                "power_classical": float(classical_power[_port_idx]),
                "mean_X_quantum": float(port_means[0]),
                "mean_P_quantum": float(port_means[1]),
                "var_X_quantum": float(port_cov[0, 0]),
                "var_P_quantum": float(port_cov[1, 1]),
                "nbar_estimate": float(photon_number_from_state(port_means, port_cov)),
            }
        )

    summary_md = build_quantum_summary_md(qstate_in, output_state, physical_ports)
    controls_md = build_active_controls_md(state_kind.value, circuit_kind.value)
    guided_observation_md = build_guided_observation_md(
        state_kind.value,
        circuit_kind.value,
        selected_mode_label,
        x_var,
        p_var,
    )
    input_means_mode0, input_cov_mode0 = input_state.modes(0)
    input_means_text = format_array(input_means_mode0)
    input_var_x = float(input_cov_mode0[0, 0])
    input_var_p = float(input_cov_mode0[1, 1])
    input_phasor_fig = plot_phasor_with_uncertainty(
        input_means_mode0,
        input_cov_mode0,
        "Input phasor + uncertainty",
    )
    output_phasor_fig = plot_phasor_with_uncertainty(
        means_mode,
        cov_mode,
        f"Selected output phasor + uncertainty ({selected_mode_label})",
    )
    phasor_bridge_md = build_phasor_bridge_md()

    return (
        circuit_details,
        classical_output,
        classical_port_names,
        classical_power,
        cov_mode,
        input_means_text,
        input_var_p,
        input_var_x,
        input_state,
        means_mode,
        mode_index,
        mode_rows,
        n_total_modes,
        nbar_mode,
        output_state,
        physical_ports,
        input_phasor_fig,
        output_phasor_fig,
        phasor_bridge_md,
        result,
        safe_wl_index,
        selected_mode_kind,
        selected_mode_label,
        summary_md,
        controls_md,
        guided_observation_md,
        x_var,
        p_var,
    )


@app.cell
def _(doc_callout_html, mo, show_interactive):
    mo.stop(not show_interactive)
    mo.md(
        r"""
        <a id="interactive"></a>
        ## Interactive studio

        The workflow below is:

        1. choose an input state,
        2. inspect its phase-space picture,
        3. send it through a simple circuit, and
        4. compare the output mean field and uncertainty.
        """
    )
    doc_callout_html(
        "info",
        tag="Experiment setup",
        title="What the notebook assumes",
        html=(
            "<p>"
            "We inject the chosen state into port <code>in0</code>. "
            "Port <code>in1</code> is explicitly initialized as vacuum, and any other required modes are "
            "filled with vacuum automatically by <code>QuantumSim</code>."
            "</p>"
            "<p>"
            "Use the new <strong>phasor + uncertainty</strong> plots to connect this notebook to your prior phasor intuition."
            "</p>"
        ),
    )
    return


@app.cell
def _(doc_callout_list, mo, show_interactive):
    mo.stop(not show_interactive)
    doc_callout_list(
        "info",
        tag="Try this",
        title="A good path through the widgets",
        items=[
            "Start with a <strong>Coherent</strong> state and the <strong>Coupler</strong> so you can match the quantum mean field to your classical intuition.",
            "Switch to <strong>Squeezed</strong> and increase `r` to see the uncertainty ellipse deform while the mean can stay similar.",
            "Switch to the <strong>MZI</strong> and vary `DeltaL` to connect interference fringes to changes in the output variances.",
        ],
    )
    return


@app.cell
def _(doc_badges, mo, n_total_modes, physical_ports, result, safe_wl_index, show_interactive, wl0_nm):
    mo.stop(not show_interactive)
    doc_badges(
        [
            f"Physical ports: <strong>{len(physical_ports)}</strong>",
            f"Total modes in output state: <strong>{n_total_modes}</strong>",
            f"Selected wavelength index: <strong>{safe_wl_index}</strong>",
            f"Center wavelength: <strong>{wl0_nm.value:.1f} nm</strong>",
            f"Simulated wavelength samples: <strong>{len(result.wl)}</strong>",
        ]
    )
    return


@app.cell
def _(controls_md, guided_observation_md, mo, phasor_bridge_md, show_interactive):
    mo.stop(not show_interactive)
    mo.vstack([mo.md(controls_md), mo.md(phasor_bridge_md), mo.md(guided_observation_md)])
    return


@app.cell
def _(doc_callout_html, input_means_text, input_var_p, input_var_x, mo, show_interactive, state_kind):
    mo.stop(not show_interactive)
    doc_callout_html(
        "info",
        tag="Input state",
        title=f"{state_kind.value} state parameters",
        html=(
            f"<p><strong>Mean vector:</strong> <code>{input_means_text}</code></p>"
            f"<p><strong>Variance in X:</strong> {input_var_x:.4f}</p>"
            f"<p><strong>Variance in P:</strong> {input_var_p:.4f}</p>"
        ),
    )
    return


@app.cell
def _(input_state, plot_single_mode):
    input_fig, input_mode_means, input_mode_cov = plot_single_mode(
        input_state,
        0,
        "Input mode in0",
    )
    return input_fig, input_mode_cov, input_mode_means


@app.cell
def _(input_fig, mo, show_interactive):
    mo.stop(not show_interactive)
    input_fig
    return


@app.cell
def _(input_phasor_fig, mo, show_interactive):
    mo.stop(not show_interactive)
    input_phasor_fig
    return


@app.cell
def _(mode_index, output_state, physical_ports, plot_single_mode):
    output_title = (
        f"Output mode {mode_index}"
        if mode_index >= len(physical_ports)
        else f"Output port {physical_ports[mode_index]}"
    )
    output_fig, output_mode_means, output_mode_cov = plot_single_mode(
        output_state,
        mode_index,
        output_title,
    )
    return output_fig, output_mode_cov, output_mode_means, output_title


@app.cell
def _(
    doc_callout_html,
    mo,
    nbar_mode,
    output_title,
    p_var,
    selected_mode_kind,
    selected_mode_label,
    show_interactive,
    x_var,
):
    mo.stop(not show_interactive)
    doc_callout_html(
        "info",
        tag="Selected mode",
        title=output_title,
        html=(
            f"<p><strong>Mode label:</strong> {selected_mode_label} ({selected_mode_kind})</p>"
            "<p><strong>Phasor interpretation:</strong> the arrow tip is the mean field, and the ellipse shows the uncertainty around that mean.</p>"
            f"<p><strong>Variance in X:</strong> {x_var:.4f}</p>"
            f"<p><strong>Variance in P:</strong> {p_var:.4f}</p>"
            f"<p><strong>Estimated photon number:</strong> {nbar_mode:.4f}</p>"
        ),
    )
    return


@app.cell
def _(mo, output_fig, show_interactive):
    mo.stop(not show_interactive)
    output_fig
    return


@app.cell
def _(mo, output_phasor_fig, show_interactive):
    mo.stop(not show_interactive)
    output_phasor_fig
    return


@app.cell
def _(
    classical_output,
    classical_port_names,
    classical_power,
    include_loss_modes,
    mode_rows,
    mo,
    np,
    physical_ports,
    plt,
    result,
    show_interactive,
):
    mo.stop(not show_interactive)

    def _match_wavelength_grid(values):
        arr = np.asarray(values, dtype=float).reshape(-1)
        if arr.size == len(wl_nm):
            return arr
        if arr.size == 1:
            return np.repeat(arr[0], len(wl_nm))
        return np.resize(arr, len(wl_nm))

    wl_nm = np.asarray(result.wl) * 1e3
    spectral_fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    ax0, ax1 = axes

    sparams = np.asarray(result.s_params)
    if "in0" in classical_port_names:
        in0_index = classical_port_names.index("in0")
        for _physical_port_name in physical_ports:
            _physical_port_idx = classical_port_names.index(_physical_port_name)
            transmission = _match_wavelength_grid(
                np.abs(sparams[:, _physical_port_idx, in0_index]) ** 2
            )
            ax0.plot(wl_nm, transmission, label=_physical_port_name)
    ax0.set_title("Classical transmission from in0")
    ax0.set_xlabel("Wavelength (nm)")
    ax0.set_ylabel("Power")
    ax0.grid(alpha=0.2)
    ax0.legend()

    cov_stack = np.asarray(result.cov)
    n_physical = len(physical_ports)
    n_modes_to_plot = cov_stack.shape[1] // 2 if include_loss_modes.value else n_physical
    for mode_idx in range(n_modes_to_plot):
        x_index = mode_idx
        p_index = mode_idx + cov_stack.shape[1] // 2
        x_var_trace = _match_wavelength_grid(cov_stack[:, x_index, x_index])
        p_var_trace = _match_wavelength_grid(cov_stack[:, p_index, p_index])
        label = (
            physical_ports[mode_idx]
            if mode_idx < n_physical
            else f"loss_mode_{mode_idx - n_physical}"
        )
        ax1.plot(wl_nm, x_var_trace, label=f"{label} : Var(X)")
        ax1.plot(wl_nm, p_var_trace, linestyle="--", alpha=0.75, label=f"{label} : Var(P)")
    ax1.set_title("Quantum variances across wavelength")
    ax1.set_xlabel("Wavelength (nm)")
    ax1.set_ylabel("Variance")
    ax1.grid(alpha=0.2)
    ax1.legend(fontsize=8, ncol=2)

    spectral_fig.tight_layout()

    table_lines = [
        "| Port | Classical alpha | Classical power | Quantum means (X, P) | Quantum vars (X, P) | nbar estimate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in mode_rows:
        classical_alpha = f"{row['alpha_classical_real']:.3f} + {row['alpha_classical_imag']:.3f}j"
        quantum_means = f"({row['mean_X_quantum']:.3f}, {row['mean_P_quantum']:.3f})"
        quantum_vars = f"({row['var_X_quantum']:.3f}, {row['var_P_quantum']:.3f})"
        table_lines.append(
            f"| {row['port']} | {classical_alpha} | {row['power_classical']:.3f} | {quantum_means} | {quantum_vars} | {row['nbar_estimate']:.3f} |"
        )

    table_md = "\n".join(table_lines)
    return classical_output, classical_power, spectral_fig, table_md


@app.cell
def _(mo, show_interactive, spectral_fig):
    mo.stop(not show_interactive)
    spectral_fig
    return

@app.cell
def _(doc_callout_html, mo, selected_mode_kind, show_interactive):
    mo.stop(not show_interactive)
    if selected_mode_kind == "loss mode":
        doc_callout_html(
            "warning",
            tag="Loss mode",
            title="Why this mode exists",
            html=(
                "<p>"
                "This mode is not a physical output port on the circuit diagram. "
                "Simphony adds it so lossy transformations can be embedded in a larger unitary model. "
                "That is why quantum loss appears as coupling to vacuum modes rather than only as reduced power."
                "</p>"
            ),
        )
    else:
        doc_callout_html(
            "info",
            tag="Physical port",
            title="How to read this mode",
            html=(
                "<p>"
                "This selected mode corresponds to a named circuit port, so it is the cleanest place to compare "
                "classical field transfer with quantum mean-field transfer."
                "</p>"
            ),
        )
    return


@app.cell
def _(mo, show_interactive, summary_md, table_md):
    mo.stop(not show_interactive)
    mo.vstack(
        [
            mo.md(summary_md),
            mo.md(table_md),
        ]
    )
    return


@app.cell
def _(doc_callout_html, mo, show_interactive):
    mo.stop(not show_interactive)
    doc_callout_html(
        "warning",
        tag="Interpretation",
        title="What to notice as you move the controls",
        html="""
        <ul>
          <li>For a <strong>coherent state</strong>, the quantum output means track the same transfer behavior as the classical field amplitude.</li>
          <li>For a <strong>squeezed state</strong>, the most obvious change is often in the <strong>variances</strong> rather than the mean.</li>
          <li>For a <strong>thermal state</strong>, the mean stays near zero while the uncertainty stays broad.</li>
          <li>Turning on circuit loss changes more than just output power: it also changes how the quantum uncertainty is carried through the network.</li>
        </ul>
        """,
    )
    return


@app.cell
def _(mo, show_entanglement):
    mo.stop(not show_entanglement)
    mo.md(
        r"""
        <a id="entanglement"></a>
        ## Entanglement preview

        Now that the single-mode picture is in place, we can add one new idea:
        two different modes can share correlated uncertainty.
        """
    )
    return


@app.cell
def _(build_entanglement_intro_md, mo, show_entanglement):
    mo.stop(not show_entanglement)
    mo.md(build_entanglement_intro_md())
    return


@app.cell
def _(mo, show_entanglement):
    mo.stop(not show_entanglement)
    ent_r = mo.ui.slider(
        start=0.0,
        stop=1.4,
        step=0.05,
        value=0.7,
        label="Two-mode squeezing strength r",
    )
    ent_thermal_n = mo.ui.slider(
        start=0.0,
        stop=2.0,
        step=0.1,
        value=0.0,
        label="Initial thermal occupation per mode",
    )
    mo.vstack([ent_r, ent_thermal_n])
    return ent_r, ent_thermal_n


@app.cell
def _(
    build_two_mode_entangled_state,
    build_two_mode_product_state,
    covariance_correlation_summary,
    ent_r,
    ent_thermal_n,
    plot_covariance_matrix,
):
    product_state = build_two_mode_product_state(ent_r.value)
    entangled_state = build_two_mode_entangled_state(ent_r.value, ent_thermal_n.value)

    product_summary = covariance_correlation_summary(product_state)
    entangled_summary = covariance_correlation_summary(entangled_state)

    product_cov_fig = plot_covariance_matrix(
        product_state,
        ["in0", "in1"],
        True,
        "Product state covariance",
    )
    entangled_cov_fig = plot_covariance_matrix(
        entangled_state,
        ["in0", "in1"],
        True,
        "Two-mode squeezed covariance",
    )

    return (
        entangled_cov_fig,
        entangled_state,
        entangled_summary,
        product_cov_fig,
        product_state,
        product_summary,
    )


@app.cell
def _(doc_callout_html, entangled_summary, product_summary, mo, show_entanglement):
    mo.stop(not show_entanglement)
    doc_callout_html(
        "info",
        tag="Compare",
        title="Product state vs correlated state",
        html=(
            "<p><strong>Independent squeezed inputs:</strong> "
            f"Cov(X0, X1) = {product_summary['x0x1']:.4f}, "
            f"Cov(P0, P1) = {product_summary['p0p1']:.4f}</p>"
            "<p><strong>Two-mode squeezed input:</strong> "
            f"Cov(X0, X1) = {entangled_summary['x0x1']:.4f}, "
            f"Cov(P0, P1) = {entangled_summary['p0p1']:.4f}</p>"
            "<p>"
            "The point of this comparison is that both cases can have large single-mode variances, "
            "but only the two-mode squeezed state develops strong off-diagonal covariance between the modes."
            "</p>"
        ),
    )
    return


@app.cell
def _(mo, product_cov_fig, show_entanglement):
    mo.stop(not show_entanglement)
    product_cov_fig
    return


@app.cell
def _(entangled_cov_fig, mo, show_entanglement):
    mo.stop(not show_entanglement)
    entangled_cov_fig
    return


@app.cell
def _(doc_callout_html, mo, show_entanglement):
    mo.stop(not show_entanglement)
    doc_callout_html(
        "warning",
        tag="Interpretation",
        title="What This Means",
        html=(
            "<p>"
            "Up to this point, you have only needed mean field plus variance. "
            "This section adds one new object: covariance between different modes."
            "</p>"
            "<p>"
            "You do not need the full formal definition of entanglement yet; the important first picture is: "
            "<strong>independent modes give block-diagonal covariance, while entangled Gaussian modes develop "
            "off-diagonal covariance blocks.</strong>"
            "</p>"
        ),
    )
    return


@app.cell
def _(mo, show_application):
    mo.stop(not show_application)
    mo.md(
        r"""
        <a id="application"></a>
        ## Practical sensing example

        Here is the practical payoff: you can use the same MZI as a sensor and ask
        how small a perturbation you can resolve.
        """
    )
    return


@app.cell
def _(doc_callout_html, mo, show_application):
    mo.stop(not show_application)
    doc_callout_html(
        "info",
        tag="Idea",
        title="Quantum-enhanced MZI sensing",
        html=(
            "<p>"
            "Suppose one arm of an MZI is exposed to temperature, strain, or a material whose refractive index changes."
            " That perturbation changes the arm phase and shifts the readout."
            "</p>"
            "<p>"
            "Below, you will compare two inputs with the <strong>same mean signal</strong>: "
            "a coherent state and a displaced squeezed state. The question is now practical:"
            " <strong>which input lets you resolve a smaller index change?</strong>"
            "</p>"
        ),
    )
    return


@app.cell
def _(mo, show_application):
    mo.stop(not show_application)
    app_alpha = mo.ui.slider(
        start=0.2,
        stop=2.0,
        step=0.1,
        value=1.0,
        label="Input displacement amplitude",
    )
    app_r = mo.ui.slider(
        start=0.0,
        stop=1.4,
        step=0.05,
        value=0.7,
        label="Squeezing strength r",
    )
    app_phi_deg = mo.ui.slider(
        start=0.0,
        stop=180.0,
        step=5.0,
        value=90.0,
        label="Squeezing angle phi (deg)",
    )
    app_sensor_length_um = mo.ui.slider(
        start=100.0,
        stop=2000.0,
        step=50.0,
        value=800.0,
        label="Sensing-arm interaction length (um)",
    )
    app_bias_delta_l = mo.ui.slider(
        start=20.0,
        stop=200.0,
        step=5.0,
        value=90.0,
        label="Bias DeltaL (um)",
    )
    app_delta_neff_span = mo.ui.slider(
        start=0.0002,
        stop=0.01,
        step=0.0002,
        value=0.003,
        label="delta n_eff sweep span",
    )
    app_readout_port = mo.ui.radio(
        options=["out0", "out1"],
        value="out0",
        label="Readout port",
        inline=True,
    )
    mo.vstack(
        [
            app_alpha,
            app_r,
            app_phi_deg,
            app_sensor_length_um,
            app_bias_delta_l,
            app_delta_neff_span,
            app_readout_port,
        ]
    )
    return (
        app_alpha,
        app_bias_delta_l,
        app_delta_neff_span,
        app_phi_deg,
        app_r,
        app_readout_port,
        app_sensor_length_um,
    )


@app.cell
def _(
    CoherentState,
    QuantumSim,
    SqueezedState,
    app_alpha,
    app_bias_delta_l,
    app_delta_neff_span,
    app_phi_deg,
    app_r,
    app_readout_port,
    app_sensor_length_um,
    build_mzi_circuit,
    compose_qstate,
    get_ports,
    jnp,
    np,
    photon_number_from_state,
    plt,
    vacuum_state,
):
    mzi_circuit = build_mzi_circuit()
    delta_neff_values = np.linspace(
        -0.5 * app_delta_neff_span.value,
        0.5 * app_delta_neff_span.value,
        31,
    )
    _wl_um = jnp.array([1.55])
    physical_ports = list(get_ports(mzi_circuit))
    port_index = physical_ports.index(app_readout_port.value)
    base_neff = 2.34
    sensor_length_um = float(app_sensor_length_um.value)
    bias_delta_l = float(app_bias_delta_l.value)

    coherent_means = []
    coherent_covariances = []
    squeezed_means = []
    squeezed_covariances = []

    for delta_neff in delta_neff_values:
        _coherent_sim = QuantumSim(
            mzi_circuit,
            wl=_wl_um,
            dc_in={"coupling": 0.5, "loss": 0.0, "phi": 0.5 * np.pi},
            dc_out={"coupling": 0.5, "loss": 0.0, "phi": 0.5 * np.pi},
            top={
                "wl0": 1.55,
                "neff": base_neff + float(delta_neff),
                "ng": 3.40,
                "length": 200.0 + bias_delta_l + sensor_length_um,
                "loss": 0.0,
            },
            bottom={"wl0": 1.55, "neff": base_neff, "ng": 3.40, "length": 200.0, "loss": 0.0},
        )

        coherent_in = compose_qstate(
            CoherentState("in0", complex(app_alpha.value, 0.0)),
            vacuum_state("in1"),
        )
        _coherent_sim.add_qstate(coherent_in)
        coherent_result = _coherent_sim.run().state(0)
        coherent_result.to_xpxp()
        _coherent_mode_means, coherent_cov = coherent_result.modes(port_index)
        coherent_means.append(np.asarray(_coherent_mode_means, dtype=float))
        coherent_covariances.append(np.asarray(coherent_cov, dtype=float))

        _squeezed_sim = QuantumSim(
            mzi_circuit,
            wl=_wl_um,
            dc_in={"coupling": 0.5, "loss": 0.0, "phi": 0.5 * np.pi},
            dc_out={"coupling": 0.5, "loss": 0.0, "phi": 0.5 * np.pi},
            top={
                "wl0": 1.55,
                "neff": base_neff + float(delta_neff),
                "ng": 3.40,
                "length": 200.0 + bias_delta_l + sensor_length_um,
                "loss": 0.0,
            },
            bottom={"wl0": 1.55, "neff": base_neff, "ng": 3.40, "length": 200.0, "loss": 0.0},
        )
        squeezed_in = compose_qstate(
            SqueezedState(
                "in0",
                r=app_r.value,
                phi=np.deg2rad(app_phi_deg.value),
                alpha=complex(app_alpha.value, 0.0),
            ),
            vacuum_state("in1"),
        )
        _squeezed_sim.add_qstate(squeezed_in)
        squeezed_result = _squeezed_sim.run().state(0)
        squeezed_result.to_xpxp()
        _squeezed_mode_means, squeezed_cov = squeezed_result.modes(port_index)
        squeezed_means.append(np.asarray(_squeezed_mode_means, dtype=float))
        squeezed_covariances.append(np.asarray(squeezed_cov, dtype=float))

    coherent_means = np.asarray(coherent_means)
    coherent_covariances = np.asarray(coherent_covariances)
    squeezed_means = np.asarray(squeezed_means)
    squeezed_covariances = np.asarray(squeezed_covariances)

    coherent_slope = np.gradient(coherent_means, delta_neff_values, axis=0)
    squeezed_slope = np.gradient(squeezed_means, delta_neff_values, axis=0)

    def _optimal_readout_metrics(means, covariances, slopes):
        readout_means = []
        readout_sigmas = []
        sensitivity_proxy = []
        readout_angles_deg = []

        for mode_means, mode_cov, mode_slope in zip(means, covariances, slopes):
            slope_norm = float(np.linalg.norm(mode_slope))
            if slope_norm < 1e-12:
                readout_direction = np.array([1.0, 0.0])
                readout_sigma = float(np.sqrt(max(mode_cov[0, 0], 0.0)))
                readout_proxy = np.inf
            else:
                regularized_cov = mode_cov + 1e-12 * np.eye(2)
                candidate_direction = np.linalg.solve(regularized_cov, mode_slope)
                candidate_norm = float(np.linalg.norm(candidate_direction))
                if candidate_norm < 1e-12:
                    readout_direction = mode_slope / slope_norm
                else:
                    readout_direction = candidate_direction / candidate_norm
                readout_variance = float(readout_direction @ mode_cov @ readout_direction)
                readout_sigma = float(np.sqrt(max(readout_variance, 0.0)))
                response = float(abs(readout_direction @ mode_slope))
                readout_proxy = readout_sigma / max(response, 1e-12)

            readout_means.append(float(readout_direction @ mode_means))
            readout_sigmas.append(readout_sigma)
            sensitivity_proxy.append(readout_proxy)
            readout_angles_deg.append(float(np.degrees(np.arctan2(readout_direction[1], readout_direction[0]))))

        return (
            np.asarray(readout_means),
            np.asarray(readout_sigmas),
            np.asarray(sensitivity_proxy),
            np.asarray(readout_angles_deg),
        )

    (
        coherent_readout_mean,
        coherent_readout_sigma,
        coherent_proxy,
        coherent_readout_angle_deg,
    ) = _optimal_readout_metrics(
        coherent_means,
        coherent_covariances,
        coherent_slope,
    )
    (
        squeezed_readout_mean,
        squeezed_readout_sigma,
        squeezed_proxy,
        squeezed_readout_angle_deg,
    ) = _optimal_readout_metrics(
        squeezed_means,
        squeezed_covariances,
        squeezed_slope,
    )
    bias_index = len(delta_neff_values) // 2

    app_signal_fig, _app_ax0 = plt.subplots(figsize=(7.2, 3.6))
    _app_ax0.plot(delta_neff_values, coherent_readout_mean, color="#2563eb", label="Coherent readout mean")
    _app_ax0.fill_between(
        delta_neff_values,
        coherent_readout_mean - coherent_readout_sigma,
        coherent_readout_mean + coherent_readout_sigma,
        color="#93c5fd",
        alpha=0.45,
        label="Coherent +/- 1 sigma",
    )
    _app_ax0.plot(delta_neff_values, squeezed_readout_mean, color="#b45309", label="Squeezed readout mean")
    _app_ax0.fill_between(
        delta_neff_values,
        squeezed_readout_mean - squeezed_readout_sigma,
        squeezed_readout_mean + squeezed_readout_sigma,
        color="#fdba74",
        alpha=0.35,
        label="Squeezed +/- 1 sigma",
    )
    _app_ax0.set_ylabel("Projected homodyne readout")
    _app_ax0.set_xlabel("delta n_eff")
    _app_ax0.set_title(f"MZI readout at {app_readout_port.value}")
    _app_ax0.grid(alpha=0.2)
    _app_ax0.legend(fontsize=8, ncol=2)
    app_signal_fig.tight_layout()

    app_proxy_fig, _app_ax1 = plt.subplots(figsize=(7.2, 3.8))
    _app_ax1.plot(delta_neff_values, coherent_proxy, color="#2563eb", label="Coherent min detectable delta n_eff")
    _app_ax1.plot(delta_neff_values, squeezed_proxy, color="#b45309", label="Squeezed min detectable delta n_eff")
    _app_ax1.set_xlabel("delta n_eff")
    _app_ax1.set_ylabel("sigma_readout / |d<readout>/d(delta n_eff)|")
    _app_ax1.set_title("Smaller is better: minimum detectable index change")
    _app_ax1.grid(alpha=0.2)
    _app_ax1.legend(fontsize=8)
    _app_ax1.text(
        0.02,
        0.02,
        "\n".join(
            [
                f"Best coherent: {float(np.min(coherent_proxy)):.3e}",
                f"Best squeezed: {float(np.min(squeezed_proxy)):.3e}",
                f"Improvement: {float(np.min(coherent_proxy) / max(np.min(squeezed_proxy), 1e-12)):.2f}x",
            ]
        ),
        transform=_app_ax1.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.9, "edgecolor": "#cbd5e1"},
    )
    app_proxy_fig.tight_layout()

    app_summary_md = "\n".join(
        [
            "### Why this matters",
            "",
            "- This models a practical photonic sensor: a small change in `n_eff` changes the interferometer phase.",
            "- The top plot shows the best homodyne readout for each state together with its uncertainty band.",
            "- At each sweep point, the notebook chooses the homodyne angle that maximizes sensitivity for that state's local mean-response vector and covariance.",
            "- The lower plot estimates the smallest resolvable `delta n_eff` using that optimal Gaussian readout.",
            "- If the squeezed curve sits lower than the coherent curve, the squeezed input is giving you a better sensing limit.",
            "",
            f"- Bias-point coherent readout angle: `{float(coherent_readout_angle_deg[bias_index]):.1f} deg`",
            f"- Bias-point squeezed readout angle: `{float(squeezed_readout_angle_deg[bias_index]):.1f} deg`",
            f"- Best coherent limit in this sweep: `{float(np.min(coherent_proxy)):.3e}`",
            f"- Best squeezed limit in this sweep: `{float(np.min(squeezed_proxy)):.3e}`",
            f"- Improvement factor (coherent / squeezed): `{float(np.min(coherent_proxy) / max(np.min(squeezed_proxy), 1e-12)):.2f}x`",
        ]
    )
    return app_proxy_fig, app_signal_fig, app_summary_md


@app.cell
def _(app_proxy_fig, app_signal_fig, app_summary_md, mo, show_application):
    mo.stop(not show_application)
    mo.vstack([app_signal_fig, app_proxy_fig, mo.md(app_summary_md)], gap=1.0)
    return


@app.cell
def _(doc_callout_list, mo, show_exercises):
    mo.stop(not show_exercises)
    mo.md(
        r"""
        <a id="exercises"></a>
        ## Short exercises
        """
    )
    doc_callout_list(
        "exercise",
        tag="Exercise 1",
        title="Coherent-state comparison",
        items=[
            "Set the input to <strong>Coherent</strong> with `alpha = 1 + 0j` and the circuit to a <strong>50/50 coupler</strong>.",
            "Compare the classical output amplitudes to the quantum output means at `out0` and `out1`.",
            "Write one sentence describing what is the same and what extra information the quantum simulation adds.",
        ],
    )

    doc_callout_list(
        "exercise",
        tag="Exercise 2",
        title="Squeezing as an uncertainty ellipse",
        items=[
            "Switch to a <strong>Squeezed</strong> state and increase `r` gradually.",
            "Watch the input and output phase-space plots.",
            "Identify which quadrature becomes narrower and which becomes wider.",
        ],
    )

    doc_callout_list(
        "exercise",
        tag="Exercise 3",
        title="Thermal state",
        items=[
            "Switch to a <strong>Thermal</strong> state and increase `nbar`.",
            "Explain why the mean vector stays near zero even though the uncertainty region grows.",
        ],
    )

    doc_callout_list(
        "exercise",
        tag="Exercise 4",
        title="MZI extension",
        items=[
            "Change the circuit to <strong>MZI</strong> and vary `DeltaL`.",
            "Use a coherent input first, then a squeezed input.",
            "Describe what changes in the transmission plot and what changes in the variance plot.",
        ],
    )

    doc_callout_list(
        "exercise",
        tag="Exercise 5",
        title="Entanglement preview",
        items=[
            "Open the <strong>Entanglement</strong> section and compare the product-state covariance plot to the two-mode squeezed covariance plot.",
            "Identify which entries are close to block-diagonal in the product state and which off-diagonal blocks become prominent in the entangled state.",
            "Write one sentence explaining what new information covariance adds beyond single-mode variances.",
        ],
    )

    doc_callout_list(
        "exercise",
        tag="Exercise 6",
        title="Quantum-enhanced sensing",
        items=[
            "Open the <strong>Application</strong> section and compare the coherent and squeezed sensing curves.",
            "Find a setting where the squeezed input gives a smaller minimum detectable `delta n_eff`.",
            "Explain in one sentence why a lower uncertainty band can improve the sensing limit even if the mean signal looks similar.",
        ],
    )
    return


@app.cell
def _(doc_callout_html, mo, show_exercises):
    mo.stop(not show_exercises)
    doc_callout_html(
        "info",
        tag="Takeaway",
        title="Takeaway",
        html=(
            "<p>"
            "A Gaussian quantum simulation keeps the familiar linear-circuit picture from classical photonics, "
            "but upgrades the notion of state from just an amplitude to <strong>mean field plus uncertainty</strong>."
            "</p>"
        ),
    )
    return


if __name__ == "__main__":
    app.run()
