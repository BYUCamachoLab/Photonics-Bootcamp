#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.17.0",
#   "gdsfactory[full]==9.25.2",
#   "simphony==0.7.3",
#   "altair==6.0.0",
#   "pyzmq",
#   "polars",
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

    section_tabs, view_state, set_view = make_section_tabs(mo)
    section_tabs
    return set_view, view_state


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_theory = view in ["All", "Theory"]
    show_interactive = view in ["All", "Interactive"]
    show_layout_section = view in ["All", "Layout"]
    return (
        show_interactive,
        show_layout_section,
        show_overview,
        show_theory,
        view,
    )


@app.cell
def _(
    doc_badges,
    show_interactive,
    show_layout_section,
    show_overview,
    show_theory,
    view,
):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
            (
                "Flags: "
                f"overview={show_overview}, "
                f"theory={show_theory}, "
                f"interactive={show_interactive}, "
                f"layout={show_layout_section}"
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
        title="MZI modelling",
        subtitle=(
            "Build intuition for a Mach–Zehnder interferometer (MZI), derive its transfer function, "
            "and connect one key layout parameter (ΔL) to a measurable signature (FSR). "
            "We’ll also preview how this maps to layout, but layout work happens in the next lesson."
        ),
        badges=[
            "Week 2",
            "Lab companion",
            "Interference",
            "Transfer functions",
            "1550 nm (default)",
            "Simphony (optional)",
            "Layout bridge",
        ],
        toc=[
            ("Overview", "overview"),
            ("Glossary", "glossary"),
            ("Theory", "theory"),
            ("Interactive", "interactive"),
            ("Layout", "layout"),
        ],
        build="2025-12-14",
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
        restore_command="git -C Photonics-Bootcamp restore marimo_course/lessons/w02_mzi_modelling.py",
        external_check_command="python3 marimo_course/lessons/check_notebook_health.py marimo_course/lessons/w02_mzi_modelling.py",
    )
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    doc_callout_list(
        "info",
        tag="Roadmap",
        title="How this notebook fits together",
        ordered=True,
        items=[
            "<strong>Analytic model:</strong> derive a simple MZI transfer function from interference.",
            "<strong>Circuit model (Simphony + SAX):</strong> build the same MZI from component (compact) models and compare.",
            "<strong>Layout (gdsfactory):</strong> transition from “response vs wavelength” to “geometry you can export as GDS”.",
        ],
    )

    doc_callout_list(
        "warning",
        tag="Quickstart",
        title="Running and troubleshooting",
        items=[
            "If you don’t see plots, make sure you’re in <strong>App view</strong> (not just the code editor), then restart/re-run the app.",
            "If <strong>Simphony</strong> isn’t available, the analytic model still works; use <em>View → Analytic only</em>.",
            "Units: the plot shows wavelength in <strong>nm</strong>; internal calculations use <strong>µm</strong>.",
        ],
    )

    doc_callout_list(
        "info",
        tag="Expected outputs",
        title="What “working” looks like (in lab)",
        items=[
            "An interactive transmission plot that changes when you move <strong>ΔL</strong>.",
            "FSR decreases when ΔL increases (approximately inverse proportional).",
            "Optional overlay with a Simphony/SAX curve if the compact-model libraries are available.",
            "A gdsfactory MZI layout preview (SVG) and a button to export a <strong>GDS</strong>.",
        ],
    )
    return


@app.cell
def _(mo, set_view, show_overview):
    mo.stop(not show_overview)
    go_interactive = mo.ui.button(
        value=0,
        kind="success",
        label="Go to Interactive section",
        on_click=lambda v: (set_view("Interactive"), (v or 0) + 1)[-1],
    )
    go_layout = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to Layout section",
        on_click=lambda v: (set_view("Layout"), (v or 0) + 1)[-1],
    )
    mo.hstack([go_interactive, go_layout])
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
def _(doc_callout_html, mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    <a id="overview"></a>
    ## What is an MZI (and why do we start here)?

    A **Mach–Zehnder interferometer (MZI)** is a small optical circuit that turns a **phase difference**
    between two paths into a **measurable power difference**.

    At a high level:
    1. A **splitter** divides the input light into two waveguides (two *arms*).
    2. The arms accumulate a **relative phase difference** (often because one arm is longer by ΔL).
    3. A **combiner** recombines the two fields, and they **interfere** at the outputs.

    **Why MZIs are useful**
    - **Sensing:** small phase shifts (temperature, strain, cladding index) become intensity changes.
    - **Modulation/switching:** if you can tune phase (thermal/electrical), an MZI becomes an optical modulator/switch.
    - **A reusable building block:** many larger photonic circuits are built from couplers + phase shifters + MZIs.

    **Why we choose MZIs as the first layout**
    - They use standard PDK primitives you’ll need all semester (splitters/combiners, waveguides, routing).
    - There’s a clean, testable signature: the arm length difference **ΔL sets the fringe spacing (FSR)**.
    - They expose key layout skills early: ports, symmetry, routing discipline, and tolerance to fabrication errors.
    """)
    doc_callout_html(
        "info",
        tag="Learning goals",
        title="What you should be able to do after this notebook",
        html="""
        <ul>
          <li>Explain how interference converts a phase difference into a power difference.</li>
          <li>Compute the ideal transfer function for a 50/50 MZI.</li>
          <li>Relate a layout parameter (ΔL) to a measurable spectral feature (FSR).</li>
        </ul>
        <p>
          This is a <strong>lab companion</strong> notebook. For graded work and “turn-in” items, use
          <code>marimo_course/assignments/hw02_mzi_modelling.py</code>.
        </p>
        """,
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    <a id="glossary"></a>
    ## Key terms (quick glossary)

    - **ΔL**: physical path-length difference between the two arms (µm).
    - **λ**: wavelength (µm here).
    - **n_eff**: (phase) effective index used in the toy phase term.
    - **n_g**: group index (sets fringe spacing / FSR).
    - **FSR**: free spectral range, the wavelength spacing between fringes.
    """)
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    ## What is gdsfactory (and why are we using it)?

    **gdsfactory** is a Python library for building **parametric photonic layouts**.
    Instead of drawing every waveguide and bend by hand, you describe a circuit using reusable components
    and parameters, and gdsfactory generates a **GDS** layout for you.

    A useful mental model:
    - A **Component** is a layout cell (like a reusable block).
    - Components have named **ports** (optical/electrical connection points).
    - You can **compose** components, route between ports, and then **export GDS**.

    **How we’ll use gdsfactory in Week 2**
    - Build a simple MZI layout from standard building blocks (splitter/combiner + waveguides).
    - Tie a *layout parameter* (ΔL) to a *measurable prediction* (FSR) from the analytic model.
    - Export a GDS file you can inspect in KLayout and eventually adapt to PDK-accurate cells for openEBL.

    In this notebook, gdsfactory is used for a small “concrete layout” example near the end.
    The more detailed layout workflow lives in `marimo_course/lessons/w02_pdk_mzi_layout.py`.
    """)
    return


@app.cell
def _(doc_callout_html, mo, show_theory):
    mo.stop(not show_theory)
    from textwrap import dedent as _dedent

    theory_md = mo.md(_dedent(r"""
    <a id="theory"></a>
    ## Analytic MZI model

    In this notebook we'll consider a symmetric 50/50 MZI with:

    - Two identical 50/50 couplers.
    - One arm longer than the other by a physical length difference ΔL (in µm).
    - A constant phase index parameter `n_eff` (toy model; we’ll refine this later).

    A simple schematic is:

    ```text
                         upper arm (longer path by ΔL)
              ┌────────┐
    Input ── ▶│ 50/50  │───────────────────────────────┐
              └───┬────┘                               │
                  │                                    │
                  │                                    │
             short arm                                 │
                  │                                    │
                  │                                    │
     Output 1 ┌───┴────┐                               │
        ◀ ────│  50/50 │───────────────────────────────┘
              └───┬────┘
                  │ Output 2
                  ▼
    ```

    The phase difference between the two arms is:

    $$
    \Delta \phi(\lambda) = \frac{2 \pi n_{\mathrm{eff}} \, \Delta L}{\lambda},
    $$

    where λ and ΔL are expressed in the same units (here, µm).

    ### Where the phase difference comes from

    A guided mode in a waveguide accumulates phase according to the propagation constant:

    $$
    \beta(\lambda) = \frac{2\pi n_{\mathrm{eff}}(\lambda)}{\lambda}.
    $$

    Over a physical path length $L$, the phase is:

    $$
    \phi(\lambda) = \beta(\lambda)\,L.
    $$

    For two arms with lengths $L_1$ and $L_2$, the *relative* phase is:

    $$
    \Delta \phi(\lambda) = \phi_2 - \phi_1 = \beta(\lambda)\,(L_2 - L_1) = \beta(\lambda)\,\Delta L.
    $$

    ### From fields to power transmission (ideal 50/50 model)

    Treat each coupler as an ideal 50/50 “beam splitter” acting on the complex field amplitudes:

    $$
    \begin{bmatrix}
    E_1 \\\\
    E_2
    \end{bmatrix}
    =
    \frac{1}{\sqrt{2}}
    \begin{bmatrix}
    1 & 1 \\\\
    1 & -1
    \end{bmatrix}
    \begin{bmatrix}
    E_{\mathrm{in}} \\\\
    0
    \end{bmatrix}
    \Rightarrow
    E_1 = \frac{E_{\mathrm{in}}}{\sqrt{2}},\;
    E_2 = \frac{E_{\mathrm{in}}}{\sqrt{2}}.
    $$

    After propagation through the two arms:

    $$
    E_1' = \frac{E_{\mathrm{in}}}{\sqrt{2}} e^{i\phi_1},\quad
    E_2' = \frac{E_{\mathrm{in}}}{\sqrt{2}} e^{i\phi_2}.
    $$

    The second 50/50 coupler recombines them:

    $$
    \begin{bmatrix}
    E_{\mathrm{through}} \\\\
    E_{\mathrm{cross}}
    \end{bmatrix}
    =
    \frac{1}{\sqrt{2}}
    \begin{bmatrix}
    1 & 1 \\\\
    1 & -1
    \end{bmatrix}
    \begin{bmatrix}
    E_1' \\\\
    E_2'
    \end{bmatrix}.
    $$

    So the through-port field is:

    $$
    E_{\mathrm{through}}
    = \frac{E_{\mathrm{in}}}{2}\left(e^{i\phi_1} + e^{i\phi_2}\right)
    = E_{\mathrm{in}}\,e^{i(\phi_1+\phi_2)/2}\cos\left(\frac{\Delta\phi}{2}\right).
    $$

    The (normalized) through-port power transmission is:

    $$
    T_{\mathrm{ideal}}(\lambda)
    = \frac{|E_{\mathrm{through}}|^2}{|E_{\mathrm{in}}|^2}
    = \cos^2\left(\frac{\Delta\phi(\lambda)}{2}\right)
    = \frac{1}{2}\left(1 + \cos \Delta \phi(\lambda)\right).
    $$

    (The other output is complementary: $T_{\mathrm{cross}} = \sin^2(\Delta\phi/2) = \frac{1}{2}(1-\cos\Delta\phi)$. Different coupler sign conventions simply swap which port you call “through” vs “cross”.)

    ### Linking ΔL to fringe spacing (FSR)

    Around a center wavelength λ₀, a useful rule of thumb is:

    $$
    \mathrm{FSR} \approx \frac{\lambda_0^2}{n_g \, \Delta L},
    $$

    where **n_g** is the group index. (This is why **n_eff** shows up in phase, but **n_g** shows up in FSR.)

    #### Derivation: where the FSR rule-of-thumb comes from

    Key idea: **adjacent fringes occur when the relative phase changes by** $2\pi$.

    Write the wavelength-dependent propagation constant as

    $$
    \beta(\lambda)=\frac{2\pi}{\lambda}n_\mathrm{eff}(\lambda),
    $$

    so the arm phase difference is

    $$
    \Delta\phi(\lambda)=\beta(\lambda)\,\Delta L.
    $$

    A “fringe-to-fringe” step in wavelength (the FSR) is the smallest $\Delta\lambda$ such that

    $$
    \Delta\phi(\lambda+\Delta\lambda)-\Delta\phi(\lambda)=2\pi.
    $$

    For small $\Delta\lambda$ we linearize:

    $$
    \frac{d\Delta\phi}{d\lambda}\,\Delta\lambda \approx 2\pi
    \quad\Rightarrow\quad
    \Delta\lambda \approx \frac{2\pi}{\Delta L\,\left|d\beta/d\lambda\right|}.
    $$

    Now differentiate $\beta(\lambda)$:

    $$
    \frac{d\beta}{d\lambda}
    =\frac{d}{d\lambda}\left(\frac{2\pi}{\lambda}n_\mathrm{eff}(\lambda)\right)
    =\frac{2\pi}{\lambda^2}\left(\lambda\frac{dn_\mathrm{eff}}{d\lambda}-n_\mathrm{eff}\right).
    $$

    Define the **group index**

    $$
    n_g \equiv n_\mathrm{eff}-\lambda\frac{dn_\mathrm{eff}}{d\lambda},
    $$

    which makes

    $$
    \left|\frac{d\beta}{d\lambda}\right|=\frac{2\pi}{\lambda^2}n_g.
    $$

    Substituting gives

    $$
    \mathrm{FSR}=\Delta\lambda \approx \frac{\lambda^2}{n_g\,\Delta L}.
    $$

    Evaluated at $\lambda=\lambda_0$, this is the rule-of-thumb used in the notebook.

    In frequency units the same idea gives $\Delta f \approx c/(n_g\,\Delta L)$, which is why this is often quoted as an “inverse length” relationship.

    Later lessons will introduce group index and propagation loss in a more realistic way.
    """))
    theory_note = doc_callout_html(
        "warning",
        tag="Note",
        title="<code>n_eff</code> vs <code>n_g</code>",
        html="""
        <p>
          The phase term uses <strong>effective index</strong> (<code>n_eff</code>), but the fringe spacing (FSR) depends on
          <strong>group index</strong> (<code>n_g</code>). In a dispersive waveguide, these are not the same.
        </p>
        """,
    )
    mo.vstack([theory_md, theory_note])
    return


@app.cell
def _(doc_callout_html, mo, show_interactive, show_theory):
    mo.stop(not (show_theory or show_interactive))
    interactive_anchor = mo.md('<a id="interactive"></a>') if show_interactive else mo.md("")
    verify_callout = doc_callout_html(
        "exercise",
        tag="Verify",
        title="Use the plot to confirm the derivation",
        html="""
        <ol>
          <li>Switch to the <strong>Interactive</strong> section using the <em>Notebook sections</em> tabs.</li>
          <li>Set <strong>ΔL = 10 µm</strong> and note the displayed <strong>FSR estimate</strong>.</li>
          <li>Double ΔL to <strong>20 µm</strong>. Prediction: the FSR should be roughly <strong>half</strong>.</li>
          <li>Use the <strong>FSR measurement tool</strong> (enter two adjacent maxima wavelengths) to measure the FSR and compare.</li>
          <li>Change <strong>base arm length</strong> (both arms equally). In the ideal model, the FSR should not change — explain why in one sentence.</li>
        </ol>
        <p><small>
          Tip: if you don’t see at least ~2 fringes, increase the spectrum span or increase ΔL.
        </small></p>
        """,
    )
    mo.vstack([interactive_anchor, verify_callout])
    return


@app.cell
def _(doc_callout_html, mo, show_theory):
    mo.stop(not show_theory)
    doc_callout_html(
        "info",
        tag="Concept check",
        title="Three quick checks before moving on",
        html="""
        <ol>
          <li>
            In the ideal analytic model here, which knob mostly changes the <em>fringe spacing</em> (FSR): <strong>ΔL</strong> or <strong>n<sub>eff</sub></strong>?
            <details><summary><em>Answer</em></summary>
              <p><strong>ΔL</strong> (and <strong>n<sub>g</sub></strong>) set the spacing; <strong>n<sub>eff</sub></strong> mostly shifts the phase / where the fringes land.</p>
            </details>
          </li>
          <li>
            Why does the FSR formula use <strong>n<sub>g</sub></strong> instead of <strong>n<sub>eff</sub></strong>?
            <details><summary><em>Answer</em></summary>
              <p>FSR comes from how quickly phase changes with wavelength, which depends on dispersion (a derivative); that derivative is captured by the <strong>group index</strong>.</p>
            </details>
          </li>
          <li>
            If the Simphony/SAX curve (when available) doesn’t match the analytic curve perfectly, name <em>one</em> likely reason.
            <details><summary><em>Answer</em></summary>
              <p>Common causes: splitter/coupler model conventions, wavelength-dependent component responses, dispersion, and loss (depending on models).</p>
            </details>
          </li>
        </ol>
        """,
    )
    return


@app.cell
def _():
    import os
    import marimo as mo
    import numpy as np
    import altair as alt
    import polars as pl
    import base64 as b64
    from pathlib import Path

    gf = None
    gf_import_error = ""
    if os.environ.get("PB_SKIP_GF") == "1":
        gf_import_error = "PB_SKIP_GF=1"
    else:
        try:
            import gdsfactory as gf
        except Exception as exc:  # pragma: no cover - depends on environment
            gf_import_error = f"{type(exc).__name__}: {exc}"

    return Path, alt, b64, gf, gf_import_error, mo, np, pl


@app.cell
def _(np):
    import ast

    _ALLOWED_FUNCS = {
        "sin",
        "cos",
        "tan",
        "exp",
        "sqrt",
        "log",
        "log10",
        "abs",
        "where",
        "clip",
        "min",
        "max",
    }

    _ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.IfExp,
        ast.Compare,
        ast.BoolOp,
        ast.And,
        ast.Or,
        ast.Not,
        ast.USub,
        ast.UAdd,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
    )

    def safe_math_eval(expression: str, env: dict):
        """Evaluate a restricted math expression (no attrs/imports/subscripts)."""

        tree = ast.parse(expression, mode="eval")

        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                raise ValueError("Attribute access is not allowed (use sin/cos/... directly).")
            if isinstance(node, ast.Subscript):
                raise ValueError("Indexing is not allowed in the playground.")
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Only direct function calls are allowed (e.g., cos(...)).")
                if node.func.id not in _ALLOWED_FUNCS:
                    raise ValueError(f"Function `{node.func.id}` is not allowed.")
                if node.keywords:
                    raise ValueError("Keyword arguments are not allowed.")
            if isinstance(node, ast.Name):
                if node.id not in env and node.id not in _ALLOWED_FUNCS:
                    raise ValueError(f"Unknown symbol `{node.id}`.")
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Unsupported syntax: {type(node).__name__}.")

        safe_globals = {"__builtins__": {}}
        safe_locals = dict(env)
        safe_locals.update(
            {
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "sqrt": np.sqrt,
                "log": np.log,
                "log10": np.log10,
                "abs": np.abs,
                "where": np.where,
                "clip": np.clip,
                "min": np.minimum,
                "max": np.maximum,
            }
        )
        code = compile(tree, "<student-expression>", "eval")
        return eval(code, safe_globals, safe_locals)  # noqa: S307 (restricted env)
    return (safe_math_eval,)


@app.cell
def _(np):
    def fsr_estimate_nm(wl0_um: float, ng: float, delta_length_um: float) -> float | None:
        if delta_length_um <= 0:
            return None
        return (wl0_um * wl0_um) / (ng * delta_length_um) * 1e3

    def phase_slope_rad_per_nm(wl0_um: float, ng: float, delta_length_um: float) -> float | None:
        if delta_length_um <= 0:
            return None
        # |dΔφ/dλ| ≈ 2π n_g ΔL / λ0^2, with λ0 and ΔL in µm.
        return (2 * np.pi * ng * delta_length_um / (wl0_um**2)) / 1e3

    def neff_linear_from_ng(
        wl_um: np.ndarray, wl0_um: float, n_eff0: float, ng: float
    ) -> tuple[np.ndarray, float]:
        # n_g = n_eff - λ dn_eff/dλ  ⇒  dn_eff/dλ = (n_eff - n_g)/λ
        dn_eff_dlambda_per_um = (n_eff0 - ng) / wl0_um
        n_eff_lambda = n_eff0 + dn_eff_dlambda_per_um * (wl_um - wl0_um)
        return n_eff_lambda, float(dn_eff_dlambda_per_um)
    return fsr_estimate_nm, neff_linear_from_ng, phase_slope_rad_per_nm


@app.cell
def _(np):
    def _local_maxima_indices(y: np.ndarray) -> np.ndarray:
        """Return indices i where y[i] is a strict local maximum."""
        y = np.asarray(y, dtype=float).reshape(-1)
        if y.size < 3:
            return np.array([], dtype=int)
        left = y[1:-1] > y[:-2]
        right = y[1:-1] >= y[2:]
        idx = np.where(left & right)[0] + 1
        return idx.astype(int)

    def auto_fsr_from_curve(
        *,
        wl_nm: np.ndarray,
        y: np.ndarray,
        wl0_nm: float,
    ) -> dict:
        """
        Detect adjacent maxima and estimate FSR near wl0.

        Returns keys:
          ok: bool
          message: str
          lam1_nm, lam2_nm, fsr_nm: float|None
          n_peaks: int
        """
        wl_nm = np.asarray(wl_nm, dtype=float).reshape(-1)
        y = np.asarray(y, dtype=float).reshape(-1)
        if wl_nm.size != y.size or wl_nm.size < 5:
            return {
                "ok": False,
                "message": "Curve data unavailable (need arrays of the same length).",
                "lam1_nm": None,
                "lam2_nm": None,
                "fsr_nm": None,
                "n_peaks": 0,
            }

        idx = _local_maxima_indices(y)
        if idx.size < 2:
            return {
                "ok": False,
                "message": "Could not find at least two maxima (try increasing ΔL or spectrum span).",
                "lam1_nm": None,
                "lam2_nm": None,
                "fsr_nm": None,
                "n_peaks": int(idx.size),
            }

        # Filter out maxima that are effectively flat due to numerical issues.
        y_min = float(np.nanmin(y))
        y_max = float(np.nanmax(y))
        y_rng = max(y_max - y_min, 0.0)
        eps = 1e-9 if y_rng == 0 else 1e-6 * y_rng
        idx = np.array([i for i in idx if (y[i] - max(y[i - 1], y[i + 1])) > eps], dtype=int)
        if idx.size < 2:
            return {
                "ok": False,
                "message": "Found maxima but they are too flat to measure reliably.",
                "lam1_nm": None,
                "lam2_nm": None,
                "fsr_nm": None,
                "n_peaks": int(idx.size),
            }

        peaks_nm = wl_nm[idx]
        peaks_nm = peaks_nm[np.argsort(peaks_nm)]
        if peaks_nm.size < 2:
            return {
                "ok": False,
                "message": "Could not compute peak spacing (unexpected).",
                "lam1_nm": None,
                "lam2_nm": None,
                "fsr_nm": None,
                "n_peaks": int(peaks_nm.size),
            }

        mids = (peaks_nm[:-1] + peaks_nm[1:]) / 2.0
        k = int(np.argmin(np.abs(mids - float(wl0_nm))))
        lam1 = float(peaks_nm[k])
        lam2 = float(peaks_nm[k + 1])
        fsr = float(abs(lam2 - lam1))

        return {
            "ok": True,
            "message": "OK",
            "lam1_nm": lam1,
            "lam2_nm": lam2,
            "fsr_nm": fsr,
            "n_peaks": int(peaks_nm.size),
        }

    return auto_fsr_from_curve,


@app.cell
def _(gf, gf_import_error, mo, show_overview):
    mo.stop(not show_overview)
    blocks = [mo.md("## gdsfactory quick check")]
    if gf is None:
        blocks.append(mo.md("`gdsfactory` is not available in this environment."))
        if gf_import_error:
            blocks.append(mo.md(f"Details: `{gf_import_error}`"))
    else:
        gf_version = getattr(gf, "__version__", None)
        if gf_version:
            blocks.append(
                mo.md(f"`gdsfactory` version (this environment): **{gf_version}**")
            )

        blocks.append(
            mo.md(
                r"""
                Minimal usage example:
                ```python
                import gdsfactory as gf
                c = gf.components.mzi(delta_length=50)  # µm
                c.write_gds("mzi.gds")
                ```
                """
            )
        )
    mo.vstack(blocks)
    return


@app.cell
def _(doc_callout_html, doc_callout_list, mo, show_interactive):
    mo.stop(not show_interactive)
    mo.md(r"""
    ## Interactive MZI spectrum

    Use the controls to explore how **ΔL** sets the **fringe spacing** (FSR).
    You can compare a simple analytic model to an optional **Simphony/SAX circuit model** built from compact component models (if available in your environment).
    """)

    doc_callout_list(
        "info",
        tag="openEBL context",
        title="Default band and why",
        items=[
            "This course’s first openEBL design targets the **1550 nm band** by default (e.g., TE 1550 grating-coupler cells in the SiEPIC EBeam PDK).",
            "So the default center wavelength here is **λ0 ≈ 1550 nm**.",
            "Advanced option: explore **1310 nm** by switching the wavelength band under **Controls → Advanced**.",
        ],
    )

    doc_callout_list(
        "info",
        tag="Assumptions",
        title="What this plot is (and isn’t)",
        items=[
            "<strong>Ideal analytic curve:</strong> lossless, perfect 50/50 couplers, and a simplified phase term with a constant <code>n_eff</code>.",
            "<strong>FSR physics:</strong> the rule-of-thumb comes from the condition “adjacent fringes ↔ Δφ changes by 2π” and uses <code>n_g</code> (group index).",
            "<strong>What’s missing:</strong> wavelength-dependent dispersion in <code>n_eff(λ)</code>, propagation loss, and non-ideal couplers (unless you use the Simphony/SAX view).",
        ],
    )

    doc_callout_html(
        "warning",
        tag="Why two curves?",
        title="Analytic vs circuit compact-model simulation",
        html="""
        <ul>
          <li><strong>Analytic</strong>: ideal, lossless, and uses a simple phase term with a tunable <code>n_eff</code>.</li>
          <li><strong>Simphony/SAX</strong>: assembles an MZI from wavelength-dependent component models (splitter + waveguides + combiner).</li>
        </ul>
        <p>
          Differences typically come from dispersion, the specific splitter/coupler model, and model conventions.
          Use the <code>n_eff</code> tuning knob to align the analytic fringe spacing near λ0.
        </p>
        """,
    )

    doc_callout_html(
        "info",
        tag="Concept check",
        title="Quick questions before you touch the sliders",
        html="""
        <ol>
          <li>
            If you <strong>double ΔL</strong>, does the FSR get bigger, smaller, or stay the same?
            <details><summary><em>Answer</em></summary><p>Smaller (approximately halves), because FSR ∝ 1/ΔL.</p></details>
          </li>
          <li>
            If you change the <strong>base arm length</strong> (both arms equally), does the FSR change in the ideal analytic model?
            <details><summary><em>Answer</em></summary><p>No. Only the <em>difference</em> ΔL changes the interference period.</p></details>
          </li>
        </ol>
        """,
    )

    doc_callout_list(
        "exercise",
        tag="Exercise",
        title="FSR vs ΔL (mini-lab)",
        ordered=True,
        items=[
            "Set ΔL to 10 µm and estimate the FSR from the plot (distance between adjacent maxima).",
            "Double ΔL. Predict the new FSR using the rule of thumb, then verify it on the plot.",
            "Change the base arm length. Does the FSR change in the ideal analytic model? Why or why not?",
        ],
    )
    return


@app.cell
def _(mo):
    base_length = mo.ui.slider(
        start=100.0,
        stop=20000.0,
        value=5000.0,
        step=100.0,
        label="Base arm length (µm)",
    )
    delta_length = mo.ui.slider(
        start=0.0,
        stop=500.0,
        value=10.0,
        step=1.0,
        label="ΔL (µm, path length difference)",
    )
    return base_length, delta_length


@app.cell
def _(mo):
    param_preset = mo.ui.dropdown(
        options=[
            "Custom (use sliders)",
            "Reset to defaults (ΔL=10 µm)",
            "ΔL = 25 µm",
            "ΔL = 50 µm",
            "ΔL = 100 µm",
        ],
        value="Custom (use sliders)",
        label="Parameter preset (overrides ΔL slider)",
    )
    return (param_preset,)


@app.cell
def _(mo):
    spectrum_center = mo.ui.slider(
        start=1.50,
        stop=1.60,
        value=1.55,
        step=0.001,
        label="Spectrum center λ0 (µm, 1550 band)",
    )
    wl_band = mo.ui.radio(
        options=[
            "1550 nm (default)",
            "1310 nm (advanced)",
        ],
        value="1550 nm (default)",
        label="Wavelength band",
        inline=True,
    )
    spectrum_center_1310 = mo.ui.slider(
        start=1.26,
        stop=1.36,
        value=1.31,
        step=0.001,
        label="Spectrum center λ0 (µm, 1310 band)",
    )
    spectrum_span_nm = mo.ui.slider(
        start=10.0,
        stop=200.0,
        value=100.0,
        step=5.0,
        label="Spectrum span (nm)",
    )
    ng = mo.ui.slider(
        start=2.0,
        stop=5.0,
        value=4.19,
        step=0.01,
        label="Group index ng (FSR estimate)",
    )
    n_eff = mo.ui.slider(
        start=1.0,
        stop=6.0,
        value=2.40,
        step=0.0001,
        label="Phase effective index n_eff (toy model; tune fringes)",
    )
    return n_eff, ng, spectrum_center, spectrum_center_1310, spectrum_span_nm, wl_band


@app.cell
def _(mo):
    view_mode = mo.ui.dropdown(
        options=[
            "Analytic only",
            "Simphony only",
            "Overlay (analytic + Simphony)",
        ],
        value="Analytic only",
        label="View",
    )
    return (view_mode,)


@app.cell
def _(mo):
    simphony_io = mo.ui.radio(
        options=[
            "Direct waveguide I/O",
            "Include grating couplers (in + out)",
        ],
        value="Direct waveguide I/O",
        label="Simphony I/O",
    )
    return (simphony_io,)


@app.cell
def _(mo):
    run_simphony = mo.ui.checkbox(
        label="Compute Simphony curve",
        value=False,
    )
    return (run_simphony,)


@app.cell
def _(mo):
    y_scale = mo.ui.radio(
        options=[
            "Linear",
            "Semilog (log y)",
        ],
        value="Linear",
        label="Y scale",
    )
    return (y_scale,)


@app.cell
def _(mo):
    show_plot_debug = mo.ui.checkbox(label="Show plot debug info", value=False)
    return (show_plot_debug,)


@app.cell
def _(mo):
    show_advanced = mo.ui.checkbox(label="Show advanced controls", value=False)
    return (show_advanced,)


@app.cell
def _(mo):
    playground_enabled = mo.ui.checkbox(
        label="Enable expression playground (student editable)",
        value=False,
    )
    playground_preset = mo.ui.radio(
        options=[
            "Ideal MZI (default)",
            "Reduced visibility (V=0.8)",
            "Add loss floor (2%)",
            "Custom",
        ],
        value="Ideal MZI (default)",
        label="Playground preset",
    )
    playground_expr = mo.ui.text_area(
        value="0.5*(1 + cos(2*pi*n_eff*delta_L/wl_um))",
        label="Custom transmission T(wl) (unitless)",
        rows=2,
    )
    return playground_enabled, playground_expr, playground_preset


@app.cell
def _(
    base_length,
    delta_length,
    mo,
    n_eff,
    ng,
    param_preset,
    playground_enabled,
    playground_expr,
    playground_preset,
    run_simphony,
    show_advanced,
    show_interactive,
    show_plot_debug,
    simphony_io,
    spectrum_center,
    spectrum_center_1310,
    spectrum_span_nm,
    wl_band,
    view_mode,
    y_scale,
):
    mo.stop(not show_interactive)
    live_update = mo.ui.checkbox(label="Live update", value=True)
    apply_update = mo.ui.button(
        value=0,
        label="Apply",
        kind="neutral",
        tooltip="When Live update is off, click Apply to recompute.",
        on_click=lambda v: (v or 0) + 1,
    )

    basic_controls = mo.vstack(
        [
            mo.hstack([spectrum_center, spectrum_span_nm]),
            mo.hstack([y_scale, view_mode]),
            mo.hstack([base_length, delta_length]),
            mo.hstack([param_preset, ng]),
            n_eff,
        ]
    )
    advanced_controls = mo.vstack(
        [
            mo.hstack([show_advanced, show_plot_debug]),
            wl_band,
            spectrum_center_1310,
            mo.hstack([playground_enabled, playground_preset]),
            playground_expr,
        ]
    )

    controls_tabs = mo.ui.tabs(
        {
            "Basic": mo.vstack([basic_controls, mo.hstack([simphony_io, run_simphony])]),
            "Advanced": advanced_controls,
        },
        value="Basic",
        lazy=True,
    )

    controls_ui = mo.vstack([mo.hstack([live_update, apply_update]), controls_tabs])
    return apply_update, controls_ui, live_update


@app.cell
def _(
    apply_update,
    base_length,
    delta_length,
    live_update,
    mo,
    n_eff,
    ng,
    param_preset,
    playground_enabled,
    playground_expr,
    playground_preset,
    run_simphony,
    show_advanced,
    show_interactive,
    show_plot_debug,
    simphony_io,
    spectrum_center,
    spectrum_center_1310,
    spectrum_span_nm,
    wl_band,
    view_mode,
    y_scale,
):
    mo.stop(not show_interactive)

    raw = {
        "base_length": float(base_length.value),
        "delta_length": float(delta_length.value),
        "param_preset": str(param_preset.value),
        "spectrum_center": float(spectrum_center.value),
        "spectrum_center_1310": float(spectrum_center_1310.value),
        "wl_band": str(wl_band.value),
        "spectrum_span_nm": float(spectrum_span_nm.value),
        "y_scale": str(y_scale.value),
        "ng": float(ng.value),
        "n_eff": float(n_eff.value),
        "view_mode": str(view_mode.value),
        "simphony_io": str(simphony_io.value),
        "run_simphony": bool(run_simphony.value),
        "show_plot_debug": bool(show_plot_debug.value),
        "show_advanced": bool(show_advanced.value),
        "playground_enabled": bool(playground_enabled.value),
        "playground_preset": str(playground_preset.value),
        "playground_expr": str(playground_expr.value or ""),
    }

    applied_state, set_applied_state = mo.state(raw)
    last_apply_click, set_last_apply_click = mo.state(0)

    if not bool(live_update.value) and int(apply_update.value) != int(last_apply_click()):
        set_applied_state(raw)
        set_last_apply_click(int(apply_update.value))

    effective = raw if bool(live_update.value) else dict(applied_state())

    _band = str(effective.get("wl_band", "1550 nm (default)"))
    if _band.startswith("1310"):
        wl0_um_effective = float(effective["spectrum_center_1310"])
    else:
        wl0_um_effective = float(effective["spectrum_center"])

    preset_deltaL_um = {
        "Reset to defaults (ΔL=10 µm)": 10.0,
        "ΔL = 25 µm": 25.0,
        "ΔL = 50 µm": 50.0,
        "ΔL = 100 µm": 100.0,
    }
    preset_label = str(effective["param_preset"])
    if preset_label in preset_deltaL_um:
        delta_length_um_effective = float(preset_deltaL_um[preset_label])
        preset_active = True
    else:
        delta_length_um_effective = float(effective["delta_length"])
        preset_active = False

    w02_params = {
        "base_length_um": float(effective["base_length"]),
        "delta_length_um_slider": float(effective["delta_length"]),
        "delta_length_um_effective": delta_length_um_effective,
        "preset_active": preset_active,
        "param_preset": preset_label,
        "wl_band": _band,
        "wl0_um": wl0_um_effective,
        "spectrum_span_nm": float(effective["spectrum_span_nm"]),
        "y_scale": str(effective["y_scale"]),
        "semilog": str(effective["y_scale"]) == "Semilog (log y)",
        "n_g": float(effective["ng"]),
        "n_eff0": float(effective["n_eff"]),
        "view_mode": str(effective["view_mode"]),
        "simphony_io": str(effective["simphony_io"]),
        "run_simphony": bool(effective["run_simphony"]),
        "show_plot_debug": bool(effective["show_plot_debug"]),
        "show_advanced": bool(effective["show_advanced"]),
        "playground_enabled": bool(effective["playground_enabled"]),
        "playground_preset": str(effective["playground_preset"]),
        "playground_expr": str(effective["playground_expr"] or ""),
        "live_update": bool(live_update.value),
        "applied": (not bool(live_update.value)) and int(apply_update.value) > 0,
    }
    return delta_length_um_effective, w02_params


@app.cell
def _(np, w02_params):
    jnp = np  # Fallback if JAX is not available.
    mzi_circuit = None
    mzi_circuit_with_gc = None
    simphony_error = ""

    needs_simphony = w02_params["view_mode"] in ["Simphony only", "Overlay (analytic + Simphony)"]
    if needs_simphony:
        try:  # pragma: no cover - depends on environment
            from jax import config

            config.update("jax_enable_x64", True)

            import jax.numpy as jnp_mod

            jnp = jnp_mod
            import sax
            from simphony.libraries import siepic

            try:  # pragma: no cover - depends on simphony / sax versions
                # Y-branch MZI: 1x2 splitter (forward) + 2x1 combiner (reverse).
                # This provides a single output port at the combiner.
                if not hasattr(siepic, "y_branch"):
                    raise AttributeError("simphony.libraries.siepic missing y_branch model")
                if not hasattr(siepic, "waveguide"):
                    raise AttributeError("simphony.libraries.siepic missing waveguide model")

                mzi_circuit, _ = sax.circuit(
                    netlist={
                        "instances": {
                            "splitter": "y_branch",
                            "short_wg": "waveguide",
                            "long_wg": "waveguide",
                            "combiner": "y_branch",
                        },
                        "connections": {
                            # Splitter outputs to arms.
                            "splitter,port_2": "short_wg,o0",
                            "splitter,port_3": "long_wg,o0",
                            # Arms into combiner (used in reverse as a 2x1 combiner).
                            "short_wg,o1": "combiner,port_2",
                            "long_wg,o1": "combiner,port_3",
                        },
                        "ports": {
                            "input": "splitter,port_1",
                            "through": "combiner,port_1",
                        },
                    },
                    models={
                        "y_branch": siepic.y_branch,
                        "waveguide": siepic.waveguide,
                    },
                )

                if hasattr(siepic, "grating_coupler"):
                    mzi_circuit_with_gc, _ = sax.circuit(
                        netlist={
                            "instances": {
                                "gc_in": "grating_coupler",
                                "splitter": "y_branch",
                                "short_wg": "waveguide",
                                "long_wg": "waveguide",
                                "combiner": "y_branch",
                                "gc_out": "grating_coupler",
                            },
                            "connections": {
                                "gc_in,o1": "splitter,port_1",
                                "combiner,port_1": "gc_out,o1",
                                # Splitter outputs to arms.
                                "splitter,port_2": "short_wg,o0",
                                "splitter,port_3": "long_wg,o0",
                                # Arms into combiner (used in reverse as a 2x1 combiner).
                                "short_wg,o1": "combiner,port_2",
                                "long_wg,o1": "combiner,port_3",
                            },
                            "ports": {
                                "input": "gc_in,o0",
                                "through": "gc_out,o0",
                            },
                        },
                        models={
                            "grating_coupler": siepic.grating_coupler,
                            "y_branch": siepic.y_branch,
                            "waveguide": siepic.waveguide,
                        },
                    )
            except Exception as e:
                mzi_circuit = None
                mzi_circuit_with_gc = None
                simphony_error = f"Simphony/SAX circuit unavailable: {e}"
        except Exception as e:
            mzi_circuit = None
            mzi_circuit_with_gc = None
            simphony_error = f"Simphony/JAX imports unavailable: {e}"
    return jnp, mzi_circuit, mzi_circuit_with_gc, simphony_error


@app.cell
def _(mo, neff_linear_from_ng, np, pl, show_interactive, w02_params):
    mo.stop(not show_interactive)
    _n_points = 400
    _wl_center_um = float(w02_params["wl0_um"])
    _span_um = float(w02_params["spectrum_span_nm"]) / 1e3
    _wl_min_um = _wl_center_um - _span_um / 2
    _wl_max_um = _wl_center_um + _span_um / 2

    _wl_um = np.linspace(_wl_min_um, _wl_max_um, _n_points)
    _wl_nm = _wl_um * 1e3

    _semilog = bool(w02_params["semilog"])
    _log_floor = 1e-6

    _n_index = float(w02_params["n_eff0"])
    _ng_for_analytic = float(w02_params["n_g"])
    _analytic_n_eff_lambda, _analytic_dn_eff_dlambda = neff_linear_from_ng(
        wl_um=_wl_um,
        wl0_um=_wl_center_um,
        n_eff0=_n_index,
        ng=_ng_for_analytic,
    )
    _delta_phi = (
        2
        * np.pi
        * _analytic_n_eff_lambda
        * float(w02_params["delta_length_um_effective"])
        / _wl_um
    )
    _T = 0.5 * (1 + np.cos(_delta_phi))
    _analytic_value_plot = np.clip(_T, _log_floor, None) if _semilog else _T

    _analytic_df = pl.DataFrame(
        {
            "wavelength_nm": _wl_nm,
            "value": _T,
            "value_plot": _analytic_value_plot,
            "curve": ["Analytic through"] * len(_wl_nm),
        }
    )

    w02_spectrum = {
        "n_points": _n_points,
        "wl_center_um": _wl_center_um,
        "wl_min_um": _wl_min_um,
        "wl_max_um": _wl_max_um,
        "wl_um": _wl_um,
        "wl_nm": _wl_nm,
        "semilog": _semilog,
        "log_floor": _log_floor,
    }
    w02_analytic = {
        "n_eff0": _n_index,
        "n_g": _ng_for_analytic,
        "dn_eff_dlambda_um_inv": float(_analytic_dn_eff_dlambda),
        "df": _analytic_df,
    }
    return w02_analytic, w02_spectrum


@app.cell
def _(mo, np, pl, safe_math_eval, show_interactive, w02_params, w02_spectrum):
    mo.stop(not show_interactive)
    _wl_um = w02_spectrum["wl_um"]
    _wl_nm = w02_spectrum["wl_nm"]
    _semilog = w02_spectrum["semilog"]
    _log_floor = w02_spectrum["log_floor"]

    _playground_error = ""
    _playground_df = None

    if bool(w02_params["playground_enabled"]):
        _preset = str(w02_params["playground_preset"])
        _preset_exprs = {
            "Ideal MZI (default)": "0.5*(1 + cos(2*pi*n_eff*delta_L/wl_um))",
            "Reduced visibility (V=0.8)": "0.5*(1 + 0.8*cos(2*pi*n_eff*delta_L/wl_um))",
            "Add loss floor (2%)": "0.02 + 0.98*0.5*(1 + cos(2*pi*n_eff*delta_L/wl_um))",
        }
        _expr_str = (
            _preset_exprs[_preset].strip()
            if _preset in _preset_exprs
            else str(w02_params["playground_expr"] or "").strip()
        )
        if not _expr_str:
            _playground_error = "Enter an expression to plot."
        else:
            try:
                _env = {
                    "wl_um": _wl_um,
                    "wl_nm": _wl_nm,
                    "pi": float(np.pi),
                    "delta_L": float(w02_params["delta_length_um_effective"]),
                    "n_eff": float(w02_params["n_eff0"]),
                    "n_g": float(w02_params["n_g"]),
                }
                _y = safe_math_eval(_expr_str, _env)
                _y_arr = np.asarray(_y, dtype=float)
                if _y_arr.shape == ():
                    _y_arr = np.full_like(_wl_um, float(_y_arr))
                else:
                    _y_arr = _y_arr.reshape(-1)
                if len(_y_arr) != len(_wl_um):
                    raise ValueError(
                        f"Expression returned {len(_y_arr)} values; expected {len(_wl_um)} (or a scalar)."
                    )

                _y_plot = np.clip(_y_arr, _log_floor, None) if _semilog else _y_arr
                _playground_df = pl.DataFrame(
                    {
                        "wavelength_nm": _wl_nm,
                        "value": _y_arr,
                        "value_plot": _y_plot,
                        "curve": ["Student expression"] * len(_wl_nm),
                    }
                )
            except Exception as e:
                _playground_error = f"{type(e).__name__}: {e}"

    w02_playground = {
        "enabled": bool(w02_params["playground_enabled"]),
        "error": _playground_error,
        "df": _playground_df,
    }
    return (w02_playground,)


@app.cell
def _(
    jnp,
    mzi_circuit,
    mzi_circuit_with_gc,
    np,
    pl,
    simphony_error,
    w02_params,
    w02_spectrum,
):
    _simphony_selected = w02_params["view_mode"] in [
        "Simphony only",
        "Overlay (analytic + Simphony)",
    ]
    _use_gratings = w02_params["simphony_io"] == "Include grating couplers (in + out)"

    _sim_circuit = None
    if _simphony_selected:
        _sim_circuit = (
            mzi_circuit_with_gc
            if (_use_gratings and mzi_circuit_with_gc is not None)
            else mzi_circuit
        )

    _wl_min_um = float(w02_spectrum["wl_min_um"])
    _wl_max_um = float(w02_spectrum["wl_max_um"])
    _n_points = int(w02_spectrum["n_points"])
    _semilog = bool(w02_spectrum["semilog"])
    _log_floor = float(w02_spectrum["log_floor"])

    _simphony_runtime_error = ""
    _simphony_plotted = False
    _sim_df = None

    _should_run = bool(w02_params["run_simphony"]) and _simphony_selected

    if _should_run and _sim_circuit is not None:
        try:
            _wl_sim = jnp.linspace(_wl_min_um, _wl_max_um, _n_points)
            _base_length_um = float(w02_params["base_length_um"])
            _delta_length_um_effective = float(w02_params["delta_length_um_effective"])

            wg_pol = "te"
            wg_width_nm = 500.0
            wg_height_nm = 220.0
            wg_loss = 0.0
            gc_pol = "te"
            gc_thickness_nm = 220.0
            gc_dwidth_nm = 0.0

            sim_kwargs = {
                "wl": _wl_sim,
                "short_wg": {
                    "length": _base_length_um,
                    "pol": wg_pol,
                    "width": wg_width_nm,
                    "height": wg_height_nm,
                    "loss": wg_loss,
                },
                "long_wg": {
                    "length": (_base_length_um + _delta_length_um_effective),
                    "pol": wg_pol,
                    "width": wg_width_nm,
                    "height": wg_height_nm,
                    "loss": wg_loss,
                },
            }

            if _use_gratings and mzi_circuit_with_gc is not None:
                sim_kwargs["gc_in"] = {
                    "pol": gc_pol,
                    "thickness": gc_thickness_nm,
                    "dwidth": gc_dwidth_nm,
                }
                sim_kwargs["gc_out"] = {
                    "pol": gc_pol,
                    "thickness": gc_thickness_nm,
                    "dwidth": gc_dwidth_nm,
                }

            S = _sim_circuit(**sim_kwargs)
            transmission_through = S["through", "input"]
            intensity_through = jnp.abs(transmission_through) ** 2

            _wl_nm = np.array(_wl_sim) * 1e3
            intensity_through_np = np.array(intensity_through)
            sim_value_plot = (
                np.clip(intensity_through_np, _log_floor, None)
                if _semilog
                else intensity_through_np
            )

            curve_label = (
                "Through (Simphony, with grating couplers)"
                if _use_gratings
                else "Through (Simphony)"
            )
            _sim_df = pl.DataFrame(
                {
                    "wavelength_nm": _wl_nm,
                    "value": intensity_through_np,
                    "value_plot": sim_value_plot,
                    "curve": [curve_label] * len(_wl_nm),
                }
            )
            _simphony_plotted = True
        except Exception as e:  # pragma: no cover
            _simphony_runtime_error = f"{type(e).__name__}: {e}"

    _simphony_status = ""
    if _simphony_selected:
        if not _should_run:
            _simphony_status = "Not computed (enable “Compute Simphony curve”)"
        elif _sim_circuit is None:
            _simphony_status = f"Unavailable: `{simphony_error}`"
        elif _simphony_runtime_error:
            _simphony_status = f"Runtime error: `{_simphony_runtime_error}`"
        elif _simphony_plotted:
            _simphony_status = "OK (Simphony curve computed)"
        else:
            _simphony_status = "No curve produced (unexpected)"

    w02_simphony = {
        "selected": _simphony_selected,
        "should_run": _should_run,
        "use_gratings": _use_gratings,
        "circuit_available": _sim_circuit is not None,
        "plotted": _simphony_plotted,
        "status": _simphony_status,
        "runtime_error": _simphony_runtime_error,
        "df": _sim_df,
        "import_error": simphony_error,
    }
    return (w02_simphony,)


@app.cell
def _(
    alt,
    controls_ui,
    fsr_estimate_nm,
    mo,
    phase_slope_rad_per_nm,
    show_interactive,
    w02_analytic,
    w02_params,
    w02_playground,
    w02_simphony,
    w02_spectrum,
):
    from _notebook_template import badge_row, download_csv_button

    mo.stop(not show_interactive)

    _wl_center_um = float(w02_spectrum["wl_center_um"])
    _wl_min_um = float(w02_spectrum["wl_min_um"])
    _wl_max_um = float(w02_spectrum["wl_max_um"])
    _semilog = bool(w02_spectrum["semilog"])
    _log_floor = float(w02_spectrum["log_floor"])

    _analytic_df = w02_analytic["df"]

    _plot_rows: list[dict] = []
    _view_mode = str(w02_params["view_mode"])
    if _view_mode in ["Analytic only", "Overlay (analytic + Simphony)"]:
        _plot_rows.extend(_analytic_df.to_dicts())

    if w02_playground.get("df") is not None:
        _plot_rows.extend(w02_playground["df"].to_dicts())

    if _view_mode in ["Simphony only", "Overlay (analytic + Simphony)"]:
        if w02_simphony.get("df") is not None:
            _plot_rows.extend(w02_simphony["df"].to_dicts())

    _base_length_um = float(w02_params["base_length_um"])
    _delta_length_um = float(w02_params["delta_length_um_effective"])
    _short_length_mm = _base_length_um / 1e3
    _long_length_mm = (_base_length_um + _delta_length_um) / 1e3

    fsr_nm = fsr_estimate_nm(
        wl0_um=_wl_center_um, ng=float(w02_params["n_g"]), delta_length_um=_delta_length_um
    )
    phase_slope_est_rad_per_nm = phase_slope_rad_per_nm(
        wl0_um=_wl_center_um, ng=float(w02_params["n_g"]), delta_length_um=_delta_length_um
    )

    fringes_est = None
    if fsr_nm is not None and fsr_nm > 0:
        fringes_est = float(w02_params["spectrum_span_nm"]) / fsr_nm

    download_button = mo.md("")
    try:
        download_button = download_csv_button(
            mo,
            _plot_rows,
            filename="mzi_spectrum.csv",
            label="Download CSV",
            preferred_fields=["wavelength_nm", "value", "value_plot", "curve"],
        )
    except Exception:  # pragma: no cover
        download_button = mo.md("")

    _sim_requested = _view_mode in ["Simphony only", "Overlay (analytic + Simphony)"]

    status_badges_list = [
        f"ΔL = <strong>{_delta_length_um:.1f} µm</strong>",
        (
            f"FSR ≈ <strong>{fsr_nm:.2f} nm</strong>"
            if fsr_nm is not None
            else "FSR: <strong>(ΔL = 0)</strong>"
        ),
    ]
    if phase_slope_est_rad_per_nm is not None:
        status_badges_list.append(
            f"|dΔφ/dλ|@λ0 ≈ <strong>{phase_slope_est_rad_per_nm:.2f} rad/nm</strong>"
        )
    status_badges_list.append(
        f"span = <strong>{float(w02_params['spectrum_span_nm']):.0f} nm</strong>"
    )
    if fringes_est is not None:
        status_badges_list.append(
            f"~ fringes in view ≈ <strong>{fringes_est:.1f}</strong>"
        )
    status_badges_list.extend(
        [
            f"View: <strong>{_view_mode}</strong>",
            f"Update: <strong>{'Live' if w02_params['live_update'] else 'Apply'}</strong>",
            (
                f"Simphony: <strong>{w02_simphony.get('status','')}</strong>"
                if _sim_requested
                else "Simphony: <strong>(not requested)</strong>"
            ),
        ]
    )
    status_badges = badge_row(
        mo, status_badges_list, style="margin: 0.35rem 0 0.25rem 0;"
    )

    if _view_mode == "Simphony only" and not w02_simphony.get("plotted", False):
        _reason_lines: list[str] = []
        if not w02_simphony.get("should_run", False):
            _reason_lines.append("Status: **Not computed** (Compute Simphony curve is off).")
            _reason_lines.append("Fix: enable **Compute Simphony curve** under Controls.")
        elif not w02_simphony.get("circuit_available", False):
            _reason_lines.append("Status: **Unavailable** (Simphony/SAX circuit not available here).")
            _reason_lines.append(f"Details: `{w02_simphony.get('import_error','')}`")
        elif w02_simphony.get("runtime_error"):
            _reason_lines.append("Status: **Runtime error** during circuit evaluation.")
            _reason_lines.append(f"Details: `{w02_simphony.get('runtime_error','')}`")
        else:
            _reason_lines.append("Status: **No curve produced** (unexpected).")
            _reason_lines.append("Fix: try toggling **Compute Simphony curve** off/on and re-run.")

        chart_out = mo.md(
            "**Simphony-only view:** no Simphony curve to display.\n\n"
            + "\n".join(f"- {line}" for line in _reason_lines)
            + "\n\nTip: switch to **Overlay** to compare with the analytic curve."
        )
    else:
        if not _plot_rows:
            _plot_rows.extend(_analytic_df.to_dicts())

        y_scale_obj = (
            alt.Scale(type="log", domain=[_log_floor, 1])
            if _semilog
            else alt.Scale(domain=[0, 1])
        )
        y_field = "value_plot" if _semilog else "value"
        chart = (
            alt.Chart(alt.Data(values=_plot_rows))
            .mark_line(point=True)
            .encode(
                x=alt.X("wavelength_nm", type="quantitative", title="Wavelength (nm)"),
                y=alt.Y(
                    y_field,
                    type="quantitative",
                    title="Through power (log scale)" if _semilog else "Through power",
                    scale=y_scale_obj,
                ),
                color=alt.Color("curve", type="nominal", title="Curve"),
                tooltip=[
                    alt.Tooltip("wavelength_nm", type="quantitative", title="Wavelength (nm)"),
                    alt.Tooltip("value", type="quantitative", title="Through power"),
                    alt.Tooltip("curve", type="nominal", title="Curve"),
                ],
            )
        ).properties(title="MZI transfer function", width=500, height=250).interactive()

        try:
            chart_out = mo.ui.altair_chart(chart) if hasattr(mo.ui, "altair_chart") else chart
        except Exception as e:  # pragma: no cover
            chart_out = mo.md(f"**Plot render error:** `{type(e).__name__}: {e}`")

    simphony_help = mo.md("")

    if w02_params.get("preset_active") and abs(
        float(w02_params["delta_length_um_slider"]) - float(w02_params["delta_length_um_effective"])
    ) > 1e-9:
        preset_note = mo.md(
            f"**ΔL preset active:** using **ΔL = {float(w02_params['delta_length_um_effective']):.1f} µm** "
            f"(slider shows {float(w02_params['delta_length_um_slider']):.1f} µm)."
        )
    else:
        preset_note = mo.md("")

    playground_error = (
        mo.md(f"**Playground error:** `{w02_playground['error']}`")
        if w02_playground.get("error")
        else mo.md("")
    )

    mo.vstack(
        [
            chart_out,
            status_badges,
            download_button,
            preset_note,
            playground_error,
            controls_ui,
            mo.md("**Next:** scroll down for the **FSR measurement tool**."),
        ]
    )
    return


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    from _notebook_template import make_fsr_tool_widgets

    auto_source, lam1_nm, lam2_nm, lam1_state, lam2_state, set_lam1, set_lam2 = (
        make_fsr_tool_widgets(mo)
    )
    return auto_source, lam1_nm, lam1_state, lam2_nm, lam2_state, set_lam1, set_lam2


@app.cell
def _(
    auto_fsr_from_curve,
    auto_source,
    doc_callout_html,
    fsr_estimate_nm,
    lam1_nm,
    lam1_state,
    lam2_nm,
    lam2_state,
    mo,
    phase_slope_rad_per_nm,
    set_lam1,
    set_lam2,
    show_interactive,
    w02_analytic,
    w02_params,
    w02_playground,
    w02_simphony,
):
    mo.stop(not show_interactive)
    wl0_um = float(w02_params["wl0_um"])
    ng_for_fsr_tool = float(w02_params["n_g"])
    dL_um = float(w02_params["delta_length_um_effective"])
    dL_slider_um = float(w02_params["delta_length_um_slider"])
    _preset_active = bool(w02_params["preset_active"])

    fsr_est_nm = fsr_estimate_nm(wl0_um=wl0_um, ng=ng_for_fsr_tool, delta_length_um=dL_um)

    measured = None
    error_pct = None
    delta_phi_est_rad = None
    delta_phi_est_cycles = None
    parse_error = ""
    try:
        if lam1_state().strip() and lam2_state().strip():
            l1 = float(lam1_state())
            l2 = float(lam2_state())
            measured = abs(l2 - l1)
            if dL_um > 0:
                fsr_tool_phase_slope = phase_slope_rad_per_nm(
                    wl0_um=wl0_um, ng=ng_for_fsr_tool, delta_length_um=dL_um
                )
                if fsr_tool_phase_slope is not None:
                    fsr_tool_two_pi = 6.283185307179586
                    delta_phi_est_rad = float(fsr_tool_phase_slope * measured)
                    delta_phi_est_cycles = float(delta_phi_est_rad / fsr_tool_two_pi)
            if fsr_est_nm is not None and fsr_est_nm > 0:
                error_pct = 100.0 * (measured - fsr_est_nm) / fsr_est_nm
    except Exception as e:
        parse_error = f"{type(e).__name__}: {e}"

    def _curve_df(source: str):
        if source == "Analytic":
            return w02_analytic.get("df"), ""
        if source == "Simphony":
            if not bool(w02_simphony.get("plotted", False)) or w02_simphony.get("df") is None:
                return None, "Simphony curve not available (compute it first, or switch view)."
            return w02_simphony["df"], ""
        if source == "Student expression":
            if not bool(w02_playground.get("enabled", False)) or w02_playground.get("df") is None:
                return None, "Student expression curve not available (enable the playground)."
            return w02_playground["df"], ""
        return None, "Unknown source."

    auto_choice = str(auto_source.value)
    if auto_choice == "Best available":
        if bool(w02_simphony.get("plotted", False)) and w02_simphony.get("df") is not None:
            auto_choice = "Simphony"
        elif bool(w02_playground.get("enabled", False)) and w02_playground.get("df") is not None:
            auto_choice = "Student expression"
        else:
            auto_choice = "Analytic"

    auto_df, auto_df_error = _curve_df(auto_choice)
    auto_result = None
    if auto_df is not None:
        try:
            wl_nm = auto_df.get_column("wavelength_nm").to_numpy()
            y = auto_df.get_column("value").to_numpy()
            auto_result = auto_fsr_from_curve(wl_nm=wl_nm, y=y, wl0_nm=float(wl0_um * 1e3))
        except Exception as e:  # pragma: no cover
            auto_df_error = f"{type(e).__name__}: {e}"

    fsr_tool_blocks = [
        doc_callout_html(
            "exercise",
            tag="Tool",
            title="Measure the FSR from the plot",
            html=r"""
            <p>
              Hover a curve to read wavelengths from the tooltip. Enter two <em>adjacent maxima</em> wavelengths
              (in nm) below; the tool computes the measured FSR and compares it to the rule-of-thumb estimate
              shown below.
            </p>
            """,
        ),
        mo.md(r"Rule-of-thumb: $\mathrm{FSR} \approx \lambda_0^2/(n_g\,\Delta L)$."),
        mo.md(
            "Derivation link: an FSR is the Δλ that makes the relative phase change by **2π** near λ0."
        ),
        mo.md(
            f"Using: **ΔL = {dL_um:.2f} µm** (effective), **λ0 = {wl0_um*1e3:.1f} nm**, **ng = {ng_for_fsr_tool:.2f}**."
        ),
        mo.hstack([auto_source]),
    ]
    if _preset_active and abs(dL_slider_um - dL_um) > 1e-9:
        fsr_tool_blocks.append(
            mo.md(
                f"**Note:** a ΔL preset is active, so the ΔL slider is ignored "
                f"(slider shows {dL_slider_um:.2f} µm). Set *Parameter preset* to **Custom** to use the slider."
            )
        )

    if auto_df_error:
        fsr_tool_blocks.append(mo.md(f"**Auto-measure ({auto_choice}):** {auto_df_error}"))
    elif isinstance(auto_result, dict) and bool(auto_result.get("ok", False)):
        _a1 = float(auto_result["lam1_nm"])
        _a2 = float(auto_result["lam2_nm"])
        _afsr = float(auto_result["fsr_nm"])
        use_auto = mo.ui.button(
            value=0,
            kind="neutral",
            label=f"Use auto peaks (λ1={_a1:.2f} nm, λ2={_a2:.2f} nm)",
            on_click=lambda v: (
                set_lam1(f"{_a1:.2f}"),
                set_lam2(f"{_a2:.2f}"),
                (v or 0) + 1,
            )[-1],
        )
        fsr_tool_blocks.append(
            mo.md(
                f"**Auto-measured FSR ({auto_choice}, {int(auto_result.get('n_peaks',0))} peaks found):** "
                f"**{_afsr:.2f} nm**"
            )
        )
        fsr_tool_blocks.append(use_auto)
    elif isinstance(auto_result, dict):
        fsr_tool_blocks.append(
            mo.md(f"**Auto-measure ({auto_choice}):** {auto_result.get('message','Could not measure.')}")
        )

    fsr_tool_blocks.append(mo.hstack([lam1_nm, lam2_nm]))

    if parse_error:
        fsr_tool_blocks.append(mo.md(f"**Parse error:** `{parse_error}`"))
    elif fsr_est_nm is None:
        fsr_tool_blocks.append(mo.md("Estimated FSR: **(ΔL = 0 → no fringes)**"))
    else:
        fsr_tool_blocks.append(
            mo.md(f"Estimated ideal FSR (using ng): **{fsr_est_nm:.2f} nm**")
        )
        if measured is not None:
            fsr_tool_blocks.append(mo.md(f"Measured FSR: **{measured:.2f} nm**"))
            if delta_phi_est_rad is not None and delta_phi_est_cycles is not None:
                fsr_tool_blocks.append(
                    mo.md(
                        f"Phase change estimate near λ0: **Δφ ≈ {delta_phi_est_rad:.2f} rad** "
                        f"(≈ **{delta_phi_est_cycles:.2f}×2π**)"
                    )
                )
            if error_pct is not None:
                fsr_tool_blocks.append(
                    mo.md(f"Percent difference vs estimate: **{error_pct:+.1f}%**")
                )
                if abs(error_pct) > 25:
                    fsr_tool_blocks.append(
                        mo.md(
                            "**Tip:** if you changed ΔL or the view mode, re-pick λ1 and λ2 from the *current* plot "
                            "(old values often produce a mismatch)."
                        )
                    )
        else:
            fsr_tool_blocks.append(
                mo.md("Enter `λ1` and `λ2` to compute the measured FSR.")
            )
    fsr_tool_view = mo.vstack([mo.md("### FSR measurement tool")] + fsr_tool_blocks)
    fsr_tool_view
    return


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    task_fsr = mo.ui.checkbox(label="Measured FSR for two ΔL values", value=False)
    task_compare = mo.ui.checkbox(label="Compared Analytic vs Simphony (Overlay)", value=False)
    task_export = mo.ui.checkbox(label="Downloaded CSV (and/or exported GDS)", value=False)
    return task_compare, task_export, task_fsr


@app.cell
def _(
    doc_callout_html,
    doc_callout_list,
    mo,
    show_interactive,
    task_compare,
    task_export,
    task_fsr,
):
    mo.stop(not show_interactive)
    doc_callout_list(
        "info",
        tag="Key ideas",
        title="What you should learn from the plot",
        items=[
            "<strong>Interference:</strong> the output power oscillates because the two arms recombine with a phase difference Δφ.",
            "<strong>ΔL sets the fringe spacing:</strong> increasing ΔL makes fringes get closer together (smaller FSR).",
            "<strong>n<sub>eff</sub> vs n<sub>g</sub>:</strong> phase uses an effective index, but FSR depends on group index (dispersion matters).",
            "<strong>Why two curves:</strong> analytic is an idealized model; Simphony/SAX assembles wavelength-dependent compact models.",
        ],
    )
    mo.md("### Checklist (before moving on)")
    mo.vstack([task_fsr, task_compare, task_export])

    doc_callout_html(
        "exercise",
        tag="Checkpoint",
        title="Record your results",
        html="""
        <p>Fill in the table below (copy into your lab notes). Use the tool above to measure FSR from two adjacent maxima.</p>
        """,
    )

    mo.md(
        r"""
        | Case | ΔL (µm) | ng | λ0 (nm) | Estimated FSR (nm) | Measured FSR (nm) | % difference |
        |---|---:|---:|---:|---:|---:|---:|
        | A (default) | 10 | 4.19 | 1550 |  |  |  |
        | B (your choice) |  |  |  |  |  |  |

        <small>Tip: if a ΔL preset is active, the notebook uses the **effective ΔL** shown in the tool readout (not the slider value).</small>
        """
    )

    doc_callout_list(
        "warning",
        tag="Common mistakes",
        title="Debugging “my FSR doesn’t match”",
        items=[
            "<strong>Preset override:</strong> if a ΔL preset is active, moving the ΔL slider won’t change the plot—set <em>Parameter preset → Custom</em>.",
            "<strong>Stale λ1/λ2:</strong> if you change ΔL, λ0, ng, or View mode, re-pick new adjacent maxima; old values won’t match.",
            "<strong>ng vs neff:</strong> <code>n_g</code> sets fringe spacing (FSR); <code>n_eff(λ0)</code> sets phase offset. Don’t expect them to do the same thing.",
            "<strong>Simphony availability:</strong> if Simphony is unavailable or errors, Overlay won’t show a second curve—check the <em>Simphony:</em> status in the Model panel.",
        ],
    )
    return


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    mo.md(r"""
    ### Guided exploration

    Try adjusting the sliders above and observe how the spectrum changes:

    - **Increase ΔL**: what happens to the fringe spacing (FSR)?
    - **Change base arm length**: does this change the fringe spacing in a lossless model?

    You can think ahead to fabrication: base arm length affects footprint (and later, loss).
    """)
    return


@app.cell
def _(mo, show_layout_section, w02_params):
    mo.stop(not show_layout_section)
    mo.md(
        r"""
        ### Connecting model and layout

        In the analytic model, the key parameter is the **path length difference** ΔL between the two arms.
        In layout, ΔL corresponds to the extra physical length you route into one arm of the interferometer.
        """
    )
    _delta_length_um_effective = float(w02_params["delta_length_um_effective"])
    if bool(w02_params["preset_active"]):
        _deltaL_note = mo.md(
            f"Analytic model currently uses ΔL = **{_delta_length_um_effective:.1f} µm** "
            f"(preset overrides slider: {float(w02_params['delta_length_um_slider']):.1f} µm)."
        )
    else:
        _deltaL_note = mo.md(
            f"Analytic model currently uses ΔL = **{_delta_length_um_effective:.1f} µm**."
        )

    _deltaL_note
    return


@app.cell
def _(mo, show_layout_section):
    mo.stop(not show_layout_section)
    mo.md(r"""
    <a id="layout"></a>
    ## From model to layout: gdsfactory

    The interactive plot above can show **two different curves** (choose *View → Overlay*):

    - **Analytic curve:** our “by-hand” ideal model, derived from interference and a simple phase term.
    - **Simphony curve:** a **circuit simulation** assembled from **component models** (compact models) using SAX.

    In the Simphony view, the MZI isn’t “drawn” — it’s built from *building blocks* (splitter, waveguides, combiner),
    where each block has a wavelength-dependent response (often represented as an **S-matrix**). SAX connects these
    blocks according to a netlist and computes the overall response.

    **So where does gdsfactory fit?**

    gdsfactory is our layout engine: it builds **geometry** (Components with ports and waveguides) and exports **GDS**.
    In this notebook, gdsfactory appears here as a transition: you’ve modelled an MZI’s behavior, and next you’ll
    learn how to *realize* an MZI in layout with the right ports, routing, and parameter control.

    This section builds a simple example MZI layout using `gf.components.mzi(...)` and shows an SVG preview inside marimo when possible. You can also export a GDS file for inspection in KLayout.
    """)
    return


@app.cell
def _(mo, show_layout_section):
    mo.stop(not show_layout_section)
    show_layout = mo.ui.checkbox(label="Show layout preview", value=True)
    gds_out = mo.ui.text(
        value="marimo_course/build/week2_mzi_example.gds",
        label="GDS output path",
    )
    export_gds = mo.ui.button(
        value=0,
        on_click=lambda v: (v or 0) + 1,
        kind="success",
        label="Write GDS",
    )
    return export_gds, gds_out, show_layout


@app.cell
def _(
    Path,
    b64,
    delta_length_um_effective,
    export_gds,
    gds_out,
    gf,
    gf_import_error,
    mo,
    show_layout,
    show_layout_section,
):
    mo.stop(not show_layout_section)
    layout_blocks = []

    c = None
    build_error = ""
    if gf is None:
        layout_blocks.append(mo.md("`gdsfactory` is not available in this environment."))
        if gf_import_error:
            layout_blocks.append(mo.md(f"Details: `{gf_import_error}`"))
    else:
        try:
            c = gf.components.mzi(delta_length=float(delta_length_um_effective))
        except Exception as e:  # pragma: no cover
            build_error = f"{type(e).__name__}: {e}"

        if c is None:
            layout_blocks.append(mo.md(f"(Could not build `gf.components.mzi`: `{build_error}`)"))
        else:
            if show_layout.value:
                svg = None
                try:
                    if hasattr(gf, "export") and hasattr(gf.export, "to_svg"):
                        svg = gf.export.to_svg(c)
                except Exception:  # pragma: no cover
                    svg = None

                if isinstance(svg, str) and "<svg" in svg:
                    svg_b64 = b64.b64encode(svg.encode("utf-8")).decode("ascii")
                    layout_blocks.extend(
                        [
                            mo.md("### Layout preview"),
                            mo.md(
                                "<div style='max-width:100%; overflow:auto;'>"
                                f"<img src='data:image/svg+xml;base64,{svg_b64}' style='max-width:100%; height:auto;'/>"
                                "</div>"
                            ),
                        ]
                    )
                else:
                    layout_blocks.append(
                        mo.md(
                            "(Preview unavailable in this environment; SVG export was not available.)"
                        )
                    )

            if export_gds.value and export_gds.value > 0:
                out_path = Path(gds_out.value).expanduser()
                out_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    written = c.write_gds(gdspath=out_path)
                    layout_blocks.append(mo.md(f"Wrote: `{written}`"))
                except Exception as e:  # pragma: no cover
                    layout_blocks.append(
                        mo.md(f"(GDS write failed: `{type(e).__name__}: {e}`)")
                    )
            else:
                layout_blocks.append(
                    mo.md("Click **Write GDS** to export the example layout.")
                )

    if not layout_blocks:
        layout_blocks.append(mo.md(""))
    mo.vstack(layout_blocks)
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    mo.md(r"""
    ## What’s next

    In `marimo_course/lessons/w02_pdk_mzi_layout.py`, you’ll shift from modelling to implementation:

    - Build an MZI layout from PDK building blocks with correct ports and routing.
    - Control ΔL in geometry and verify it matches the modelling intuition from this notebook.
    - Export GDS and inspect it (KLayout), preparing for more realistic PDK-accurate circuits.

    In upcoming modelling lessons, we’ll add realism step-by-step:

    - **Dispersion:** use a wavelength-dependent `n_eff(λ)` so `n_g` emerges naturally (and FSR becomes a local approximation).
    - **Loss + visibility:** include propagation loss (and later, imbalance) so fringes aren’t perfectly 0–1.
    - **Non-ideal couplers:** explore splitter imbalance and phase conventions, and how they affect “through vs cross”.
    - **Tuning/modulation:** connect phase tuning (thermal/electrical) to a shift in the interference pattern.
    """)
    return


if __name__ == "__main__":
    app.run()
