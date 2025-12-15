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
    mo.md(r"""
    <style>
      :root {
        --doc-max: 920px;
        --doc-muted: color-mix(in srgb, currentColor 65%, transparent);
        --doc-border: color-mix(in srgb, currentColor 18%, transparent);
        --doc-accent: #2563eb;
        --doc-bg: color-mix(in srgb, currentColor 3%, transparent);
      }

      /* "Docs-like" typography + width */
      .markdown.prose,
      .markdown.prose > :is(h1,h2,h3,h4,h5,h6,p,ul,ol,pre,blockquote,table,hr,div) {
        max-width: var(--doc-max);
      }
      .markdown.prose { padding-right: 1rem; }
      .markdown.prose :is(h1,h2,h3) { letter-spacing: -0.01em; }
      .markdown.prose a { color: var(--doc-accent); text-decoration: none; }
      .markdown.prose a:hover { text-decoration: underline; }
      .markdown.prose code {
        background: var(--doc-bg);
        padding: 0.12rem 0.28rem;
        border-radius: 0.3rem;
      }
      .markdown.prose pre code { background: transparent; padding: 0; }
      .markdown.prose pre {
        border: 1px solid var(--doc-border);
        border-radius: 0.7rem;
        padding: 0.9rem 1rem;
        overflow: auto;
      }

      .doc-hero {
        max-width: var(--doc-max);
        border: 1px solid var(--doc-border);
        border-radius: 1rem;
        padding: 1.2rem 1.2rem 0.9rem 1.2rem;
        background: linear-gradient(
          180deg,
          color-mix(in srgb, var(--doc-accent) 10%, transparent),
          transparent
        );
      }
      .doc-hero h1 { margin: 0.2rem 0 0.4rem 0; }
      .doc-hero p { margin: 0.2rem 0 0.8rem 0; color: var(--doc-muted); }
      .doc-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.2rem 0; }
      .doc-badge {
        border: 1px solid var(--doc-border);
        border-radius: 999px;
        padding: 0.15rem 0.55rem;
        font-size: 0.85rem;
        background: color-mix(in srgb, currentColor 2%, transparent);
      }
      .doc-toc {
        max-width: var(--doc-max);
        border: 1px solid var(--doc-border);
        border-radius: 0.9rem;
        padding: 0.8rem 1rem;
        background: color-mix(in srgb, currentColor 1%, transparent);
      }
      .doc-toc ul { margin: 0.4rem 0 0 1.2rem; }

      /* Standard callouts */
      .callout {
        max-width: var(--doc-max);
        border: 1px solid var(--doc-border);
        border-radius: 0.9rem;
        padding: 0.85rem 1rem;
        margin: 0.9rem 0;
        background: color-mix(in srgb, currentColor 1%, transparent);
      }
      .callout-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
      }
      .callout-title .tag {
        font-size: 0.8rem;
        border: 1px solid var(--doc-border);
        border-radius: 999px;
        padding: 0.1rem 0.5rem;
        color: var(--doc-muted);
        font-weight: 600;
      }
      .callout.info { border-left: 5px solid #2563eb; }
      .callout.warning { border-left: 5px solid #b45309; }
      .callout.exercise { border-left: 5px solid #059669; }

      /* Slightly more compact widgets (sliders/buttons/inputs) */
      label, input, select, textarea, button {
        font-size: 0.92rem;
      }

      @media (max-width: 980px) {
        .markdown.prose { padding-right: 1rem; }
      }
    </style>
    """)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        <div class="doc-hero">
          <div class="doc-badges">
            <span class="doc-badge">Week 2</span>
            <span class="doc-badge">Interference</span>
            <span class="doc-badge">Transfer functions</span>
            <span class="doc-badge">gdsfactory + Simphony</span>
          </div>
          <h1>MZI modelling with gdsfactory</h1>
          <p>Build intuition for a Mach–Zehnder interferometer (MZI), derive its transfer function, and connect one key layout parameter (ΔL) to a measurable signature (FSR).</p>
          <p><small><em>Notebook build: 2025-12-14</em></small></p>
        </div>
        """
    )
    mo.md(
        r"""
        <div class="doc-toc">
          <strong>On this page</strong>
          <ul>
            <li><a href="#mzi-intro">What is an MZI?</a></li>
            <li><a href="#glossary">Key terms</a></li>
            <li><a href="#gdsfactory">What is gdsfactory?</a></li>
            <li><a href="#theory">Analytic model</a></li>
            <li><a href="#interactive">Interactive spectrum</a></li>
            <li><a href="#layout">Layout preview + GDS export</a></li>
          </ul>
        </div>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    <div class="callout info">
      <div class="callout-title">
        <span class="tag">Roadmap</span>
        <span>How this notebook fits together</span>
      </div>
      <ol>
        <li><strong>Analytic model:</strong> derive a simple MZI transfer function from interference.</li>
        <li><strong>Circuit model (Simphony + SAX):</strong> build the same MZI from component (compact) models and compare.</li>
        <li><strong>Layout (gdsfactory):</strong> transition from “response vs wavelength” to “geometry you can export as GDS”.</li>
      </ol>
    </div>

    <div class="callout warning">
      <div class="callout-title">
        <span class="tag">Quickstart</span>
        <span>Running and troubleshooting</span>
      </div>
      <ul>
        <li>If you don’t see plots, make sure you’re in <strong>App view</strong> (not just the code editor), then restart/re-run the app.</li>
        <li>If <strong>Simphony</strong> isn’t available, the analytic model still works; use <em>View → Analytic only</em>.</li>
        <li>Units: the plot shows wavelength in <strong>nm</strong>; internal calculations use <strong>µm</strong>.</li>
      </ul>
    </div>

    <div class="callout info">
      <div class="callout-title">
        <span class="tag">Expected outputs</span>
        <span>What “working” looks like</span>
      </div>
      <ul>
        <li>An interactive transmission plot that changes when you move <strong>ΔL</strong>.</li>
        <li>FSR decreases when ΔL increases (approximately inverse proportional).</li>
        <li>Optional overlay with a Simphony/SAX curve if the compact-model libraries are available.</li>
        <li>A gdsfactory MZI layout preview (SVG) and a button to export a <strong>GDS</strong>.</li>
      </ul>
    </div>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="mzi-intro"></a>
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

    <div class="callout info">
      <div class="callout-title">
        <span class="tag">Learning goals</span>
        <span>What you should be able to do after this notebook</span>
      </div>
      <ul>
        <li>Explain how interference converts a phase difference into a power difference.</li>
        <li>Compute the ideal transfer function for a 50/50 MZI.</li>
        <li>Relate a layout parameter (ΔL) to a measurable spectral feature (FSR).</li>
      </ul>
      <p><strong>Deliverables:</strong></p>
      <ul>
        <li>A screenshot (or saved image) of an MZI spectrum showing at least 2 fringes.</li>
        <li>Your measured FSR from the plot and your predicted FSR from the rule-of-thumb equation.</li>
      </ul>
    </div>
    """)
    return


@app.cell
def _(mo):
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
def _(mo):
    mo.md(r"""
    <a id="gdsfactory"></a>
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
def _(mo):
    mo.md(r"""
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

    Later lessons will introduce group index and propagation loss in a more realistic way.

    <div class="callout warning">
      <div class="callout-title">
        <span class="tag">Note</span>
        <span><code>n_eff</code> vs <code>n_g</code></span>
      </div>
      <p>
        The phase term uses <strong>effective index</strong> (<code>n_eff</code>), but the fringe spacing (FSR) depends on
        <strong>group index</strong> (<code>n_g</code>). In a dispersive waveguide, these are not the same.
      </p>
    </div>
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    import gdsfactory as gf
    import polars as pl
    return alt, gf, mo, np, pl


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
    return safe_math_eval


@app.cell
def _(gf, mo):
    gf_version = getattr(gf, "__version__", None)
    mo.md("## gdsfactory quick check")
    if gf_version:
        mo.md(f"`gdsfactory` version (this environment): **{gf_version}**")
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
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="interactive"></a>
    ## Interactive MZI spectrum

    Use the controls to explore how **ΔL** sets the **fringe spacing** (FSR).
    You can compare a simple analytic model to an optional **Simphony/SAX circuit model** built from compact component models (if available in your environment).

    <div class="callout warning">
      <div class="callout-title">
        <span class="tag">Why two curves?</span>
        <span>Analytic vs circuit compact-model simulation</span>
      </div>
      <ul>
        <li><strong>Analytic</strong>: ideal, lossless, and uses a simple phase term with a tunable <code>n_eff</code>.</li>
        <li><strong>Simphony/SAX</strong>: assembles an MZI from wavelength-dependent component models (splitter + waveguides + combiner).</li>
      </ul>
      <p>
        Differences typically come from dispersion, the specific splitter/coupler model, and model conventions.
        Use the <code>n_eff</code> tuning knob to align the analytic fringe spacing near λ0.
      </p>
    </div>

    <div class="callout exercise">
      <div class="callout-title">
        <span class="tag">Exercise</span>
        <span>FSR vs ΔL (mini-lab)</span>
      </div>
      <ol>
        <li>Set ΔL to 10 µm and estimate the FSR from the plot (distance between adjacent maxima).</li>
        <li>Double ΔL. Predict the new FSR using the rule of thumb, then verify it on the plot.</li>
        <li>Change the base arm length. Does the FSR change in the ideal analytic model? Why or why not?</li>
      </ol>
    </div>
    """)
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
        label="Parameter preset",
    )
    return param_preset


@app.cell
def _(delta_length, param_preset):
    preset_deltaL_um = {
        "Reset to defaults (ΔL=10 µm)": 10.0,
        "ΔL = 25 µm": 25.0,
        "ΔL = 50 µm": 50.0,
        "ΔL = 100 µm": 100.0,
    }
    preset_label = param_preset.value
    if preset_label in preset_deltaL_um:
        delta_length_um_effective = float(preset_deltaL_um[preset_label])
        preset_active = True
    else:
        delta_length_um_effective = float(delta_length.value)
        preset_active = False
    return delta_length_um_effective, preset_active


@app.cell
def _(mo):
    spectrum_center = mo.ui.slider(
        start=1.50,
        stop=1.60,
        value=1.55,
        step=0.001,
        label="Spectrum center λ0 (µm)",
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
    return n_eff, ng, spectrum_center, spectrum_span_nm


@app.cell
def _(mo):
    view_mode = mo.ui.radio(
        options=[
            "Analytic only",
            "Simphony only",
            "Overlay (analytic + Simphony)",
        ],
        value="Analytic only",
        label="View",
    )
    return view_mode


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
    return simphony_io


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
    return y_scale


@app.cell
def _(mo):
    show_plot_debug = mo.ui.checkbox(label="Show plot debug info", value=False)
    return show_plot_debug


@app.cell
def _(mo):
    show_advanced = mo.ui.checkbox(label="Show advanced controls", value=False)
    return show_advanced


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
def _(np, view_mode):
    jnp = np  # Fallback if JAX is not available.
    mzi_circuit = None
    mzi_circuit_with_gc = None
    simphony_error = ""

    needs_simphony = view_mode.value in ["Simphony only", "Overlay (analytic + Simphony)"]
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
def _(
    alt,
    base_length,
    delta_length,
    delta_length_um_effective,
    jnp,
    mo,
    mzi_circuit,
    mzi_circuit_with_gc,
    n_eff,
    ng,
    np,
    param_preset,
    pl,
    playground_enabled,
    playground_expr,
    playground_preset,
    preset_active,
    safe_math_eval,
    show_advanced,
    show_plot_debug,
    simphony_error,
    simphony_io,
    spectrum_center,
    spectrum_span_nm,
    view_mode,
    y_scale,
):
    n_points = 400

    wl_center_um = float(spectrum_center.value)
    span_um = float(spectrum_span_nm.value) / 1e3
    wl_min_um = wl_center_um - span_um / 2
    wl_max_um = wl_center_um + span_um / 2

    wl = np.linspace(wl_min_um, wl_max_um, n_points)

    # Analytic MZI model (lossless, constant index parameter).
    #
    # Note: the SiEPIC waveguide compact model used by Simphony is dispersive. Here we
    # keep a constant index parameter chosen to match the approximate FSR near 1550 nm
    # for the default SiEPIC TE strip waveguide (500 nm x 220 nm).
    n_index = float(n_eff.value)
    delta_phi = 2 * np.pi * n_index * float(delta_length_um_effective) / wl
    T = 0.5 * (1 + np.cos(delta_phi))

    semilog = y_scale.value == "Semilog (log y)"
    log_floor = 1e-6
    analytic_value_plot = np.clip(T, log_floor, None) if semilog else T

    analytic_df = pl.DataFrame(
        {
            "wavelength_nm": wl * 1e3,
            "value": T,
            "value_plot": analytic_value_plot,
            "curve": ["Analytic through"] * len(wl),
        }
    )

    try:
        analytic_data = analytic_df.to_pandas()
    except Exception:
        # Altair expects table-like data; use row dicts when pandas isn't available.
        analytic_data = analytic_df.to_dicts()

    # Vega-Lite in the VS Code marimo viewer can be fragile with layered Altair charts.
    # Build a single "long" table and plot everything with one chart.
    plot_rows: list[dict] = []

    if view_mode.value in ["Analytic only", "Overlay (analytic + Simphony)"]:
        plot_rows.extend(analytic_df.to_dicts())

    playground_error = ""
    if playground_enabled.value:
        preset = playground_preset.value
        preset_exprs = {
            "Ideal MZI (default)": "0.5*(1 + cos(2*pi*n_eff*delta_L/wl_um))",
            "Reduced visibility (V=0.8)": "0.5*(1 + 0.8*cos(2*pi*n_eff*delta_L/wl_um))",
            "Add loss floor (2%)": "0.02 + 0.98*0.5*(1 + cos(2*pi*n_eff*delta_L/wl_um))",
        }
        expr_str = (
            preset_exprs[preset].strip()
            if preset in preset_exprs
            else (playground_expr.value or "").strip()
        )
        if not expr_str:
            playground_error = "Enter an expression to plot."
        else:
            try:
                env = {
                    "wl_um": wl,
                    "wl_nm": wl * 1e3,
                    "pi": float(np.pi),
                    "delta_L": float(delta_length_um_effective),
                    "n_eff": float(n_index),
                    "n_g": float(ng.value),
                }
                y = safe_math_eval(expr_str, env)
                y_arr = np.asarray(y, dtype=float)
                if y_arr.shape == ():
                    y_arr = np.full_like(wl, float(y_arr))
                else:
                    y_arr = y_arr.reshape(-1)
                if len(y_arr) != len(wl):
                    raise ValueError(
                        f"Expression returned {len(y_arr)} values; expected {len(wl)} (or a scalar)."
                    )

                y_plot = np.clip(y_arr, log_floor, None) if semilog else y_arr
                user_df = pl.DataFrame(
                    {
                        "wavelength_nm": wl * 1e3,
                        "value": y_arr,
                        "value_plot": y_plot,
                        "curve": ["Student expression"] * len(wl),
                    }
                )
                plot_rows.extend(user_df.to_dicts())
            except Exception as e:
                playground_error = f"{type(e).__name__}: {e}"

    simphony_selected = view_mode.value in ["Simphony only", "Overlay (analytic + Simphony)"]
    use_gratings = simphony_io.value == "Include grating couplers (in + out)"

    # Guard against any environment/editor issues where the Simphony cell fails to
    # define these symbols; in that case, Simphony view gracefully becomes unavailable.
    mzi_circuit_local = locals().get("mzi_circuit", None)
    mzi_circuit_with_gc_local = locals().get("mzi_circuit_with_gc", None)

    sim_circuit = None
    if simphony_selected:
        sim_circuit = (
            mzi_circuit_with_gc_local
            if (use_gratings and mzi_circuit_with_gc_local is not None)
            else mzi_circuit_local
        )

    if simphony_selected and sim_circuit is not None:
        # Simphony MZI model using SAX / siepic library.
        wl_sim = jnp.linspace(wl_min_um, wl_max_um, n_points)

        # NOTE: simphony's SiEPIC library uses microns for geometric parameters like `length`,
        # and nanometers for `width`/`height`.
        base_length_um = float(base_length.value)

        # SiEPIC compact-model parameters (explicitly passed so the notebook is reproducible).
        wg_pol = "te"
        wg_width_nm = 500.0
        wg_height_nm = 220.0
        wg_loss = 0.0
        gc_pol = "te"
        gc_thickness_nm = 220.0
        gc_dwidth_nm = 0.0

        sim_kwargs = {
            "wl": wl_sim,
            "short_wg": {
                "length": base_length_um,
                "pol": wg_pol,
                "width": wg_width_nm,
                "height": wg_height_nm,
                "loss": wg_loss,
            },
            "long_wg": {
                "length": (base_length_um + float(delta_length_um_effective)),
                "pol": wg_pol,
                "width": wg_width_nm,
                "height": wg_height_nm,
                "loss": wg_loss,
            },
        }

        if use_gratings and mzi_circuit_with_gc is not None:
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

        S = sim_circuit(**sim_kwargs)

        transmission_through = S["through", "input"]
        intensity_through = jnp.abs(transmission_through) ** 2

        wl_nm = np.array(wl_sim) * 1e3
        intensity_through_np = np.array(intensity_through)
        sim_value_plot = (
            np.clip(intensity_through_np, log_floor, None) if semilog else intensity_through_np
        )

        curve_label = (
            "Through (Simphony, with grating couplers)" if use_gratings else "Through (Simphony)"
        )
        sim_df = pl.DataFrame(
            {
                "wavelength_nm": wl_nm,
                "value": intensity_through_np,
                "value_plot": sim_value_plot,
                "curve": [curve_label] * len(wl_nm),
            }
        )
        plot_rows.extend(sim_df.to_dicts())

    if not plot_rows:
        plot_rows.extend(analytic_df.to_dicts())

    y_scale_obj = (
        alt.Scale(type="log", domain=[log_floor, 1]) if semilog else alt.Scale(domain=[0, 1])
    )
    y_field = "value_plot" if semilog else "value"
    # Inline data explicitly; passing a raw list can be rejected by Altair depending on version.
    chart = (
        alt.Chart(alt.Data(values=plot_rows))
        .mark_line(point=True)
        .encode(
            x=alt.X("wavelength_nm", type="quantitative", title="Wavelength (nm)"),
            y=alt.Y(
                y_field,
                type="quantitative",
                title="Through power (log scale)" if semilog else "Through power",
                scale=y_scale_obj,
            ),
            color=alt.Color("curve", type="nominal", title="Curve"),
            tooltip=[
                alt.Tooltip("wavelength_nm", type="quantitative", title="Wavelength (nm)"),
                alt.Tooltip("value", type="quantitative", title="Through power"),
                alt.Tooltip("curve", type="nominal", title="Curve"),
            ],
        )
    )

    chart = chart.properties(
        title="MZI transfer function",
        width=500,
        height=250,
    ).interactive()

    base_length_um = float(base_length.value)
    delta_length_um = float(delta_length_um_effective)
    short_length_mm = base_length_um / 1e3
    long_length_mm = (base_length_um + delta_length_um) / 1e3

    fsr_nm = None
    if delta_length_um > 0:
        fsr_nm = (wl_center_um * wl_center_um) / (float(ng.value) * delta_length_um) * 1e3

    left_items = [
        mo.md("**Spectrum**"),
        spectrum_center,
        spectrum_span_nm,
        y_scale,
        mo.md(f"Wavelength window: **{wl_min_um*1e3:.1f}–{wl_max_um*1e3:.1f} nm**"),
        mo.md("**Geometry**"),
        base_length,
        delta_length,
        param_preset,
        *(
            [
                mo.md(
                    f"Preset active: using **ΔL = {delta_length_um_effective:.1f} µm** "
                    "(set preset to *Custom* to use the slider)."
                )
            ]
            if preset_active
            else []
        ),
        ng,
        mo.md(r"FSR rule of thumb: $\mathrm{FSR} \approx \lambda_0^2 / (n_g\,\Delta L)$"),
        mo.md(
            "Estimated ideal FSR: "
            + (
                f"**{fsr_nm:.2f} nm** (using ng)"
                if fsr_nm is not None
                else "**(ΔL = 0 → no fringes)**"
            )
        ),
        mo.md(f"Lengths: short={short_length_mm:.2f} mm, long={long_length_mm:.2f} mm"),
    ]

    if semilog:
        left_items.append(mo.md(f"Semilog note: values are floored at **{log_floor:g}** for display."))

    right_items = [
        mo.md("**Model**"),
        view_mode,
        show_advanced,
        show_plot_debug,
    ]

    if view_mode.value in ["Simphony only", "Overlay (analytic + Simphony)"]:
        right_items.append(simphony_io)

    if view_mode.value in ["Simphony only", "Overlay (analytic + Simphony)"] and mzi_circuit is None:
        right_items.append(
            mo.md(
                "**Note:** Simphony-based circuit view is unavailable in this environment.\n\n"
                f"`{simphony_error}`"
            )
        )

    if show_advanced.value:
        right_items.extend(
            [
                mo.md("#### Analytic tuning"),
                n_eff,
                mo.md(f"Analytic phase uses `n_eff = {n_index:.5f}`."),
                mo.md("#### Student playground"),
                playground_enabled,
            ]
        )

        if playground_enabled.value:
            right_items.append(playground_preset)
            if playground_preset.value == "Custom":
                right_items.append(playground_expr)
            right_items.append(
                mo.md(
                    r"""
                    <div class="callout info">
                      <div class="callout-title">
                        <span class="tag">Playground</span>
                        <span>How it works</span>
                      </div>
                      <p>The dashed curve is computed from your preset/expression and plotted alongside the analytic/Simphony curves.</p>
                      <p>Use these variables: <code>wl_um</code>, <code>wl_nm</code>, <code>delta_L</code>, <code>n_eff</code>, <code>n_g</code>, <code>pi</code>.</p>
                      <p>Allowed functions: <code>sin</code>, <code>cos</code>, <code>tan</code>, <code>exp</code>, <code>sqrt</code>, <code>log</code>, <code>log10</code>, <code>abs</code>, <code>where</code>, <code>clip</code>, <code>min</code>, <code>max</code>.</p>
                      <p><strong>Tip:</strong> Expressions may return a scalar (applied to all wavelengths) or an array with the same length as <code>wl_um</code>.</p>
                    </div>
                    """
                )
            )
            if playground_error:
                right_items.append(mo.md(f"**Playground error:** `{playground_error}`"))
    else:
        right_items.append(mo.md(f"Analytic phase tuning uses `n_eff = {n_index:.5f}`."))

    if show_plot_debug.value:
        try:
            y_key = "value_plot" if semilog else "value"
            y_vals = np.array([r.get(y_key) for r in plot_rows if r.get("curve") == "Analytic through"], dtype=float)
            finite = y_vals[np.isfinite(y_vals)]
            y_min = float(np.min(finite)) if finite.size else None
            y_max = float(np.max(finite)) if finite.size else None
        except Exception:
            y_min = None
            y_max = None
        right_items.append(
            mo.md(
                f"**Debug:** rows={len(plot_rows)}; analytic {y_key} min/max={y_min}/{y_max}"
            )
        )

    try:
        chart_out = mo.ui.altair_chart(chart) if hasattr(mo.ui, "altair_chart") else chart
    except Exception as e:  # pragma: no cover
        chart_out = mo.md(f"**Plot render error:** `{type(e).__name__}: {e}`")
    controls = mo.hstack([mo.vstack(left_items), mo.vstack(right_items)])
    fringes_est = None
    if fsr_nm is not None and fsr_nm > 0:
        fringes_est = float(spectrum_span_nm.value) / fsr_nm

    download_badge = ""
    try:
        import base64
        import csv
        import io

        if plot_rows:
            out = io.StringIO()
            preferred_fields = ["wavelength_nm", "value", "value_plot", "curve"]
            extra_fields = sorted(
                {
                    k
                    for row in plot_rows
                    for k in row.keys()
                    if k not in preferred_fields
                }
            )
            fieldnames = preferred_fields + extra_fields
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            for row in plot_rows:
                writer.writerow({k: row.get(k, "") for k in fieldnames})
            csv_b64 = base64.b64encode(out.getvalue().encode("utf-8")).decode("ascii")
            download_badge = (
                "<a class=\"doc-badge\" "
                "style=\"cursor:pointer;\" "
                "download=\"mzi_spectrum.csv\" "
                f"href=\"data:text/csv;base64,{csv_b64}\">"
                "<strong>Download CSV</strong>"
                "</a>"
            )
    except Exception:  # pragma: no cover
        download_badge = ""

    fsr_badge = (
        f'<span class="doc-badge">FSR ≈ <strong>{fsr_nm:.2f} nm</strong></span>'
        if fsr_nm is not None
        else '<span class="doc-badge">FSR: <strong>(ΔL = 0)</strong></span>'
    )
    fringes_badge = (
        f'<span class="doc-badge">~ fringes in view ≈ <strong>{fringes_est:.1f}</strong></span>'
        if fringes_est is not None
        else ""
    )
    status_badges = mo.md(
        f"""
        <div class="doc-badges" style="margin: 0.35rem 0 0.25rem 0;">
          <span class="doc-badge">ΔL = <strong>{delta_length_um_effective:.1f} µm</strong></span>
          {fsr_badge}
          <span class="doc-badge">span = <strong>{float(spectrum_span_nm.value):.0f} nm</strong></span>
          {fringes_badge}
          <span class="doc-badge">View: <strong>{view_mode.value}</strong></span>
          {download_badge}
        </div>
        """
    )
    mo.vstack(
        [
            chart_out,
            status_badges,
            mo.md("### Controls"),
            controls,
        ]
    )
    return


@app.cell
def _(mo):
    lam1_nm = mo.ui.text(value="", label="λ1 (nm)")
    lam2_nm = mo.ui.text(value="", label="λ2 (nm)")
    return lam1_nm, lam2_nm


@app.cell
def _(delta_length_um_effective, lam1_nm, lam2_nm, mo, ng, spectrum_center):
    wl0_um = float(spectrum_center.value)
    ng_val = float(ng.value)
    dL_um = float(delta_length_um_effective)

    fsr_est_nm = None
    if dL_um > 0:
        fsr_est_nm = (wl0_um * wl0_um) / (ng_val * dL_um) * 1e3

    measured = None
    error_pct = None
    parse_error = ""
    try:
        if lam1_nm.value.strip() and lam2_nm.value.strip():
            l1 = float(lam1_nm.value)
            l2 = float(lam2_nm.value)
            measured = abs(l2 - l1)
            if fsr_est_nm is not None and fsr_est_nm > 0:
                error_pct = 100.0 * (measured - fsr_est_nm) / fsr_est_nm
    except Exception as e:
        parse_error = f"{type(e).__name__}: {e}"

    blocks = [
        mo.md(
            r"""
            <div class="callout exercise">
              <div class="callout-title">
                <span class="tag">Tool</span>
                <span>Measure the FSR from the plot</span>
              </div>
              <p>
                Hover a curve to read wavelengths from the tooltip. Enter two <em>adjacent maxima</em> wavelengths
                (in nm) below; the tool computes the measured FSR and compares it to the rule-of-thumb estimate
                $\mathrm{FSR} \approx \lambda_0^2/(n_g\,\Delta L)$.
              </p>
            </div>
            """
        ),
        mo.hstack([lam1_nm, lam2_nm]),
    ]

    if parse_error:
        blocks.append(mo.md(f"**Parse error:** `{parse_error}`"))
    elif fsr_est_nm is None:
        blocks.append(mo.md("Estimated FSR: **(ΔL = 0 → no fringes)**"))
    else:
        blocks.append(mo.md(f"Estimated ideal FSR (using ng): **{fsr_est_nm:.2f} nm**"))
        if measured is not None:
            blocks.append(mo.md(f"Measured FSR: **{measured:.2f} nm**"))
            if error_pct is not None:
                blocks.append(mo.md(f"Percent difference vs estimate: **{error_pct:+.1f}%**"))
        else:
            blocks.append(mo.md("Enter `λ1` and `λ2` to compute the measured FSR."))
    return


@app.cell
def _(mo):
    task_fsr = mo.ui.checkbox(label="Measured FSR for two ΔL values", value=False)
    task_compare = mo.ui.checkbox(label="Compared Analytic vs Simphony (Overlay)", value=False)
    task_export = mo.ui.checkbox(label="Downloaded CSV (and/or exported GDS)", value=False)
    return task_compare, task_export, task_fsr


@app.cell
def _(mo, task_compare, task_export, task_fsr):
    mo.md(
        r"""
        <div class="callout info">
          <div class="callout-title">
            <span class="tag">Key ideas</span>
            <span>What you should learn from the plot</span>
          </div>
          <ul>
            <li><strong>Interference:</strong> the output power oscillates because the two arms recombine with a phase difference Δφ.</li>
            <li><strong>ΔL sets the fringe spacing:</strong> increasing ΔL makes fringes get closer together (smaller FSR).</li>
            <li><strong>n<sub>eff</sub> vs n<sub>g</sub>:</strong> phase uses an effective index, but FSR depends on group index (dispersion matters).</li>
            <li><strong>Why two curves:</strong> analytic is an idealized model; Simphony/SAX assembles wavelength-dependent compact models.</li>
          </ul>
        </div>
        """
    )
    mo.md("### Checklist (before moving on)")
    mo.vstack([task_fsr, task_compare, task_export])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Guided exploration

    Try adjusting the sliders above and observe how the spectrum changes:

    - **Increase ΔL**: what happens to the fringe spacing (FSR)?
    - **Change base arm length**: does this change the fringe spacing in a lossless model?

    You can think ahead to fabrication: base arm length affects footprint (and later, loss).
    """)
    return


@app.cell
def _(delta_length, delta_length_um_effective, mo, preset_active):
    mo.md(
        r"""
        ### Connecting model and layout

        In the analytic model, the key parameter is the **path length difference** ΔL between the two arms.
        In layout, ΔL corresponds to the extra physical length you route into one arm of the interferometer.
        """
    )
    if preset_active:
        mo.md(
            f"Analytic model currently uses ΔL = **{delta_length_um_effective:.1f} µm** "
            f"(preset overrides slider: {delta_length.value:.1f} µm)."
        )
    else:
        mo.md(f"Analytic model currently uses ΔL = **{delta_length_um_effective:.1f} µm**.")
    return


@app.cell
def _(mo):
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
def _(mo):
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
    return show_layout, gds_out, export_gds


@app.cell
def _(delta_length_um_effective, export_gds, gf, gds_out, mo, show_layout):
    import base64
    from pathlib import Path

    blocks = []

    c = None
    build_error = ""
    try:
        c = gf.components.mzi(delta_length=float(delta_length_um_effective))
    except Exception as e:  # pragma: no cover
        build_error = f"{type(e).__name__}: {e}"

    if c is None:
        return mo.md(f"(Could not build gf.components.mzi: `{build_error}`)")

    if show_layout.value:
        svg = None
        try:
            if hasattr(gf, "export") and hasattr(gf.export, "to_svg"):
                svg = gf.export.to_svg(c)
        except Exception:  # pragma: no cover
            svg = None

        if isinstance(svg, str) and "<svg" in svg:
            b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
            blocks.extend(
                [
                    mo.md("### Layout preview"),
                    mo.md(
                        "<div style='max-width:100%; overflow:auto;'>"
                        f"<img src='data:image/svg+xml;base64,{b64}' style='max-width:100%; height:auto;'/>"
                        "</div>"
                    ),
                ]
            )
        else:
            blocks.append(
                mo.md("(Preview unavailable in this environment; SVG export was not available.)")
            )

    if export_gds.value and export_gds.value > 0:
        out_path = Path(gds_out.value).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            written = c.write_gds(gdspath=out_path)
            blocks.append(mo.md(f"Wrote: `{written}`"))
        except Exception as e:  # pragma: no cover
            blocks.append(mo.md(f"(GDS write failed: `{type(e).__name__}: {e}`)"))
    else:
        blocks.append(mo.md("Click **Write GDS** to export the example layout."))

    return mo.vstack(blocks)


@app.cell
def _(mo):
    mo.md(r"""
    <a id="next"></a>
    ## What’s next

    In `marimo_course/lessons/w02_pdk_mzi_layout.py`, you’ll shift from modelling to implementation:

    - Build an MZI layout from PDK building blocks with correct ports and routing.
    - Control ΔL in geometry and verify it matches the modelling intuition from this notebook.
    - Export GDS and inspect it (KLayout), preparing for more realistic PDK-accurate circuits.
    """)
    return


if __name__ == "__main__":
    app.run()
