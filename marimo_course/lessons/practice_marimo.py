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
