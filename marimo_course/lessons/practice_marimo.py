# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.17.0",
#     "numpy",
#     "altair",
#     "polars",
#     "pyzmq",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # Practice marimo

    This is a low-stakes sandbox to practice marimo features:

    - Reactive UI controls (`mo.ui.slider`, `mo.ui.radio`)
    - Layout (`mo.hstack`, `mo.vstack`)
    - A simple MZI-style interference model
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0) Basics (first-time users)

    These cells show how marimo connects UI controls to live output.
    """)
    return


@app.cell
def _(mo):
    name = mo.ui.text(value="Ada", label="Your name")
    excited = mo.ui.checkbox(value=True, label="Add excitement")
    clicks = mo.ui.button(value=0, label="Click me", kind="success")
    mo.hstack([name, excited, clicks])
    return clicks, excited, name


@app.cell
def _(clicks, excited, mo, name):
    suffix = "!" if excited.value else "."
    mo.md(
        f"Hello **{name.value}**{suffix} Button clicks: **{clicks.value}**"
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0b) Simple math (reactive)

    Change the sliders and watch the math update.
    """)
    return


@app.cell
def _(mo):
    radius = mo.ui.slider(start=0.0, stop=5.0, value=2.0, step=0.1, label="Radius (cm)")
    scale = mo.ui.slider(start=1, stop=10, value=3, step=1, label="Scale factor")
    mo.hstack([radius, scale])
    return radius, scale


@app.cell
def _(mo, radius, scale):
    r = float(radius.value)
    area = 3.14159 * r * r
    scaled = area * float(scale.value)
    mo.md(
        f"Circle area: **{area:.2f} cm²**  |  Scaled area: **{scaled:.2f} cm²**"
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0c) Small table

    A tiny table built from Python data.
    """)
    return


@app.cell
def _(mo):
    rows = [
        {"task": "Install Python", "time_min": 10, "done": False},
        {"task": "Run marimo", "time_min": 5, "done": False},
        {"task": "Open Week 1", "time_min": 5, "done": False},
    ]
    mo.ui.table(rows)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0d) Tiny plot

    A small reactive plot using Altair.
    """)
    return


@app.cell
def _(mo):
    points = mo.ui.slider(start=5, stop=50, value=12, step=1, label="Number of points")
    mo.hstack([points])
    return (points,)


@app.cell
def _(alt, mo, np, points, pl):
    n = int(points.value)
    x = np.linspace(0, 2 * np.pi, n)
    df = pl.DataFrame({"x": x, "y": np.sin(x)})
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("x:Q", title="x"),
            y=alt.Y("y:Q", title="sin(x)"),
            tooltip=[alt.Tooltip("x:Q", format=".2f"), alt.Tooltip("y:Q", format=".2f")],
        )
        .properties(width=420, height=220)
    )
    mo.vstack([chart])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1) ASCII schematic (reactive)

    Use the slider to choose a path-length difference ΔL and see it reflected in the schematic.
    """)
    return


@app.cell
def _(mo):
    delta_length = mo.ui.slider(
        start=0.0,
        stop=500.0,
        value=50.0,
        step=5.0,
        label="ΔL (µm)",
    )
    return (delta_length,)


@app.cell
def _(delta_length, mo):
    dl_schematic = float(delta_length.value)
    mo.md(
        f"""
```text
                     upper arm (extra length = ΔL = {dl_schematic:.1f} µm)
          ┌────────┐
Input ──▶ │ 50/50  │───────────────────────────────────────────┐
          └───┬────┘                                           │
              │                                                │
              │                                                │
         short arm                                             │
              │                                                │
              │                                                │
 Output  ┌────┴────┐                                           │
  ──────▶│ 50/50   │───────────────────────────────────────────┘
          └────────┘
```
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2) Simple spectrum (reactive)

    This is a toy model (lossless, constant index parameter) to practice reactive plotting.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    import polars as pl
    return alt, mo, np, pl


@app.cell
def _(mo):
    y_scale = mo.ui.radio(
        options=["Linear", "Semilog (log y)"],
        value="Linear",
        label="Y scale",
    )
    center_wl = mo.ui.slider(
        start=1.50,
        stop=1.60,
        value=1.55,
        step=0.001,
        label="λ0 for FSR estimate (µm)",
    )
    ng = mo.ui.slider(
        start=2.0,
        stop=5.0,
        value=4.19,
        step=0.01,
        label="Group index ng (FSR estimate)",
    )
    return center_wl, ng, y_scale


@app.cell
def _(alt, center_wl, delta_length, mo, ng, np, pl, y_scale):
    wl_min_um = 1.50
    wl_max_um = 1.60
    wl = np.linspace(wl_min_um, wl_max_um, 600)

    n_index = 4.19088
    delta_phi = 2 * np.pi * n_index * delta_length.value / wl
    T = 0.5 * (1 + np.cos(delta_phi))

    semilog = y_scale.value == "Semilog (log y)"
    log_floor = 1e-6
    T_plot = np.clip(T, log_floor, None) if semilog else T

    df = pl.DataFrame(
        {
            "wavelength_nm": wl * 1e3,
            "T": T,
            "T_plot": T_plot,
        }
    )

    y = alt.Y(
        "T_plot:Q",
        title="Through power (log)" if semilog else "Through power",
        scale=alt.Scale(type="log") if semilog else alt.Scale(zero=False),
    )

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("wavelength_nm:Q", title="Wavelength (nm)"),
            y=y,
            tooltip=[
                alt.Tooltip("wavelength_nm:Q", title="Wavelength (nm)", format=".1f"),
                alt.Tooltip("T:Q", title="Through power", format=".4f"),
            ],
        )
        .properties(width=520, height=260, title="Toy MZI spectrum")
        .interactive()
    )

    controls = mo.vstack(
        [
            delta_length,
            mo.md(
                r"FSR rule of thumb: $\mathrm{FSR} \approx \lambda_0^2 / (n_g\,\Delta L)$"
            ),
            center_wl,
            ng,
            y_scale,
            mo.md(f"Wavelength window: **{wl_min_um*1e3:.0f}–{wl_max_um*1e3:.0f} nm**"),
        ]
    )

    dl_fsr = float(delta_length.value)
    if dl_fsr > 0:
        fsr_nm = (float(center_wl.value) ** 2) / (float(ng.value) * dl_fsr) * 1e3
        fsr_line = mo.md(f"Estimated ideal FSR: **{fsr_nm:.2f} nm**")
    else:
        fsr_line = mo.md("Estimated ideal FSR: **(ΔL = 0 → no fringes)**")

    mo.vstack([fsr_line, mo.hstack([controls, chart])])
    return


if __name__ == "__main__":
    app.run()
