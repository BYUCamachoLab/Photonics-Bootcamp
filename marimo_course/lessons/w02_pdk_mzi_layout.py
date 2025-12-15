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
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    klayout_open = mo.ui.checkbox(label="KLayout open with SiEPIC-EBeam-PDK", value=False)
    placed_couplers = mo.ui.checkbox(
        label="Placed I/O couplers and splitter/combiner", value=False
    )
    routed_skeleton = mo.ui.checkbox(label="Routed simple MZI skeleton", value=False)
    built_parametric = mo.ui.checkbox(
        label="Built parametric MZI in gdsfactory (optional)", value=False
    )
    saved_design = mo.ui.checkbox(label="Saved design in openEBL-2026-02 repo", value=False)
    return (
        built_parametric,
        klayout_open,
        placed_couplers,
        routed_skeleton,
        saved_design,
    )


@app.cell
def _(
    built_parametric,
    klayout_open,
    placed_couplers,
    routed_skeleton,
    saved_design,
):
    checks = [
        klayout_open,
        placed_couplers,
        routed_skeleton,
        built_parametric,
        saved_design,
    ]
    completed = sum(int(c.value) for c in checks)
    progress = completed / len(checks) if checks else 0.0
    progress_bar = (
        "<div style='margin:10px 0 6px; border:1px solid rgba(120,120,120,0.35);"
        " border-radius:999px; height:12px; overflow:hidden;'>"
        f"<div style='height:100%; width:{progress*100:.1f}%;"
        " background: rgba(31,111,235,0.70);'></div>"
        "</div>"
    )
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    center_wl = mo.ui.slider(
        start=1.50,
        stop=1.60,
        value=1.55,
        step=0.001,
        label="Target center wavelength (µm)",
    )
    ng = mo.ui.slider(
        start=2.0,
        stop=5.0,
        value=4.19,
        step=0.01,
        label="Estimated group index (ng)",
    )
    delta_length = mo.ui.slider(
        start=1.0,
        stop=1000.0,
        value=50.0,
        step=1.0,
        label="Planned ΔL in layout (µm)",
    )
    return (delta_length,)


app._unparsable_cell(
    r"""

        lam0 = float(center_wl.value)
        n_g = float(ng.value)
        dL = float(delta_length.value)

        if dL <= 0:
            return mo.md(\\"Choose a non-zero ΔL to estimate the FSR.\\")

        fsr_um = lam0 * lam0 / (n_g * dL)
        fsr_nm = fsr_um * 1e3
        summary = (
            f\\"For ΔL = **{dL:.1f} µm** and ng = **{n_g:.2f}** at \\"
            f\\"λ0 = **{lam0:.3f} µm**, the ideal FSR is ≈ **{fsr_nm:.1f} nm**.\\"
        )
    
    """,
    name="_"
)


@app.cell
def _():
    from pathlib import Path
    return (Path,)


@app.cell
def _():
    try:
        import gdsfactory as gf  # type: ignore

        gf_import_error = None
    except Exception as e:  # pragma: no cover
        gf = None
        gf_import_error = f"{type(e).__name__}: {e}"
    return gf, gf_import_error


@app.cell
def _():
    return


@app.cell
def _(mo):
    workflow_stage = mo.ui.radio(
        options={
            "spec": "1) Pick targets (FSR ↔ ΔL)",
            "gen": "2) Generate a skeleton GDS (gdsfactory)",
            "klayout": "3) Open in KLayout + load PDK",
            "annotate": "4) Add pins/labels/floorplan",
            "save": "5) Save into openEBL repo",
        },
        value="spec",
        label="Workflow step",
    )
    return (workflow_stage,)


@app.cell
def _(Path, mo):
    default_out = Path("marimo_course/build/week2_mzi_skeleton.gds")
    gds_path = mo.ui.text(
        value=str(default_out),
        label="GDS output path",
    )
    length_x = mo.ui.slider(
        start=1.0,
        stop=200.0,
        value=60.0,
        step=1.0,
        label="MZI base length_x (µm)",
    )
    length_y = mo.ui.slider(
        start=1.0,
        stop=50.0,
        value=10.0,
        step=0.5,
        label="MZI base length_y (µm)",
    )
    export_gds = mo.ui.button(
        value=0,
        on_click=lambda v: (v or 0) + 1,
        kind="success",
        label="Generate / overwrite GDS",
    )
    controls = mo.vstack([gds_path, length_x, length_y, export_gds])
    return controls, export_gds, gds_path, length_x, length_y


@app.cell
def _(
    Path,
    controls,
    delta_length,
    export_gds,
    gds_path,
    gf,
    gf_import_error,
    length_x,
    length_y,
    mo,
    workflow_stage,
):
    import inspect

    stage = workflow_stage.value
    blocks = []

    if stage == "spec":
        blocks.append(
            mo.md(
                r"""
                **Goal:** pick a ΔL that gives a reasonable FSR for the wavelength range you care about.

                Use the sliders above (λ0, ng, ΔL) and sanity-check against the Week 2 modelling notebook.
                """
            )
        )

    elif stage == "gen":
        if gf is None:
            blocks.extend(
                [
                    mo.md(
                        r"""
                        <div class="pb-callout">
                        <strong>gdsfactory not available in this environment.</strong><br/>
                        This step requires a local Python environment with <code>gdsfactory</code> installed.
                        </div>
                        """
                    ),
                    mo.md(f"Import error: `{gf_import_error}`"),
                    mo.md("Suggested install (local venv): `pip install gdsfactory`"),
                ]
            )
        else:
            blocks.extend(
                [
                    mo.md(
                        r"""
                        **What this generates:** a parametric MZI skeleton using gdsfactory’s standard components.

                        - Units: gdsfactory lengths are in **µm**
                        - Ports: the exported cell will have optical ports like `o1`, `o2`
                        """
                    ),
                    controls,
                ]
            )

            mzi_factory = gf.components.mzi
            sig = inspect.signature(mzi_factory)
            param_names = set(sig.parameters)

            kwargs: dict[str, float] = {}
            if "delta_length" in param_names:
                kwargs["delta_length"] = float(delta_length.value)
            elif "delta_length_um" in param_names:
                kwargs["delta_length_um"] = float(delta_length.value)

            if "length_x" in param_names:
                kwargs["length_x"] = float(length_x.value)
            if "length_y" in param_names:
                kwargs["length_y"] = float(length_y.value)

            c = mzi_factory(**kwargs)

            if export_gds.value is None or export_gds.value <= 0:
                blocks.append(mo.md("Click **Generate / overwrite GDS** to write the file."))
            else:
                out_path = Path(gds_path.value).expanduser()
                out_path.parent.mkdir(parents=True, exist_ok=True)

                written = c.write_gds(gdspath=out_path)
                blocks.extend(
                    [
                        mo.md(f"Wrote: `{written}`"),
                        mo.md(f"Next: open it in KLayout: `klayout {written}`"),
                    ]
                )

    elif stage == "klayout":
        blocks.append(
            mo.md(
                r"""
                **KLayout steps:**
                1. Launch KLayout.
                2. Ensure the **SiEPIC-EBeam-PDK** is installed and selected.
                3. Open the generated GDS (or your design GDS) and inspect geometry + layers.
                4. Keep this notebook open to cross-check ΔL and expected FSR.
                """
            )
        )

    elif stage == "annotate":
        blocks.append(
            mo.md(
                r"""
                **Annotation steps (what CI/tools typically need):**
                - Add/verify **Pins** (PinRec) and **Device recognition** (DevRec) on the top-level cell.
                - Add text labels for device name, student ID, and ports (if your flow expects it).
                - Add a **floorplan** / die boundary if required by the openEBL submission rules.
                """
            )
        )

    elif stage == "save":
        blocks.append(
            mo.md(
                r"""
                **Save + repo steps:**
                - Place your final GDS in the `openEBL-2026-02` repo (per the course instructions).
                - Run whatever verification/CI checks are required by the run repo.
                - Keep a copy of the “skeleton” parameters (ΔL, length_x, length_y) in your notes.
                """
            )
        )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
