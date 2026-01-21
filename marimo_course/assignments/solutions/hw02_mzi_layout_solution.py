#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.19.0",
#   "pyzmq",
#   "gdsfactory",
#   "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import sys
    import pathlib as pathlib_assign
    import marimo as mo

    assignments_dir = pathlib_assign.Path(__file__).resolve().parents[1]
    if str(assignments_dir) not in sys.path:
        sys.path.insert(0, str(assignments_dir))

    from _assignment_template import load_lesson_template, _ensure_lessons_on_path

    _ensure_lessons_on_path()
    from _notebook_template import optional_import

    inject_css, make_doc_helpers, make_health_refresh_button, header = load_lesson_template()

    inject_css(mo)

    doc_badges, doc_callout_html, doc_callout_list = make_doc_helpers(mo)
    return doc_callout_list, header, mo


@app.cell(hide_code=True)
def _(header, mo):
    header(
        mo,
        title="HW02 — Solution: MZI layout + openEBL prep",
        subtitle=(
            "Reference solution for building an MZI layout in Python using the SiEPIC-EBeam PDK cells, "
            "then adding PinRec/DevRec/labels and exporting a submission-ready GDS."
        ),
        badges=["Week 2", "Homework", "Solution", "PDK layout", "openEBL prep"],
        toc=[
            ("Overview", "overview"),
            ("Build MZI", "build"),
            ("Add Submission Layers", "layers"),
            ("Export", "export"),
        ],
        build="2026-01-16",
    )
    return


@app.cell(hide_code=True)
def _(doc_callout_list, mo):
    overview_md = mo.md(r"""
    <a id="overview"></a>
    ## Overview

    This homework guides you through **building your own MZI layout** and preparing it
    for openEBL submission. You will:

    1. Choose PDK cells for the splitter/combiner and grating couplers.
    2. Build an MZI with a chosen ΔL.
    3. Add PinRec, DevRec, and Text labels.
    4. Export a submission-ready GDS.
    """)

    solution_note = doc_callout_list(
        "warning",
        tag="Solution",
        title="Instructor reference",
        items=[
            "This notebook is a filled-in example. Students should complete the assignment in the main homework notebook.",
        ],
    )

    submission_checklist = doc_callout_list(
        "info",
        tag="What to submit",
        title="Submission checklist",
        items=[
            "Your exported GDS in `openEBL-2026-02/submissions/` (named per run rules).",
            "A screenshot of the final layout (showing ports + DevRec).",
            "Both output ports are present and labeled in the final GDS.",
            "Short note: your ΔL and target FSR.",
        ],
    )
    return (mo.vstack([overview_md, solution_note, submission_checklist]),)


@app.cell(hide_code=True)
def _(overview_md):
    overview_md
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tasks (do these in order)

    1. **Simphony (single output):** Use Simphony + SAX to plot the spectrum for the
       single output port in the starter layout.
    2. **Layout update:** Add a second output port to your layout GDS and make the
       layout submission‑ready (PinRec, DevRec, labels, Floorplan if required).
    3. **Simphony (both outputs):** Update your circuit model to expose both outputs
       and plot both spectra (through + cross).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="build"></a>
    ## Build MZI (PDK cells + routing)

    **Edit the parameters below.** The starter layout exposes a single output;
    you will add a second output port later in the assignment.
    """)
    return


@app.cell
def _(mo):
    # SOLUTION VALUES — update if your paths differ
    import pathlib as pathlib_params

    username = "solution_user"
    repo_root = pathlib_params.Path(__file__).resolve().parents[3]
    ebeam_pdk_path = str(repo_root / "SiEPIC_EBeam_PDK_public")
    openebl_path = str(repo_root / "openEBL-2026-02")

    delta_length_um = 300.0
    length_x_um = 60.0
    length_y_um = 10.0

    splitter_gds = f"{ebeam_pdk_path}/klayout/EBeam/gds/EBeam/ebeam_y_1550.gds"
    splitter_cell = "ebeam_y_1550"

    combiner_gds = f"{ebeam_pdk_path}/klayout/EBeam/gds/EBeam/ebeam_bdc_te1550.gds"
    combiner_cell = "ebeam_bdc_te1550"

    gc_gds = f"{ebeam_pdk_path}/klayout/EBeam/gds/EBeam/ebeam_gc_te1550.gds"
    gc_cell = "ebeam_gc_te1550"

    export_gds = f"{openebl_path}/submissions/EBeam_{username}.gds"

    mo.md(
        f"- ΔL: `{delta_length_um}` µm\n"
        f"- length_x: `{length_x_um}` µm\n"
        f"- length_y: `{length_y_um}` µm\n"
        f"- splitter cell: `{splitter_cell}`\n"
        f"- combiner cell: `{combiner_cell}`\n"
        f"- GC cell: `{gc_cell}`\n"
        f"- export path: `{export_gds}`\n"
    )
    return (
        delta_length_um,
        export_gds,
        combiner_cell,
        combiner_gds,
        gc_cell,
        gc_gds,
        length_x_um,
        length_y_um,
        splitter_cell,
        splitter_gds,
    )


@app.cell
def _(
    delta_length_um,
    combiner_cell,
    combiner_gds,
    gc_cell,
    gc_gds,
    length_x_um,
    length_y_um,
    mo,
    splitter_cell,
    splitter_gds,
):
    import pathlib as pathlib_hw
    import gdsfactory as gf
    from gdsfactory.add_ports import add_ports_from_markers_center
    from gdsfactory.read import import_gds
    from gdsfactory.port import auto_rename_ports_orientation

    gf.clear_cache()
    gf.gpdk.PDK.activate()
    c = None

    xs = gf.cross_section.strip(layer=(1, 0), width=0.5)

    # Check for GDS files
    splitter_path = pathlib_hw.Path(splitter_gds)
    combiner_path = pathlib_hw.Path(combiner_gds)
    gc_path = pathlib_hw.Path(gc_gds)
    mo.stop(
        not splitter_path.exists(),
        mo.md(f"Error: Splitter GDS not found: `{splitter_path}`")
    )
    mo.stop(
        not combiner_path.exists(),
        mo.md(f"Error: Combiner GDS not found: `{combiner_path}`")
    )
    mo.stop(
        not gc_path.exists(),
        mo.md(f"Error: GC GDS not found: `{gc_path}`")
    )

    splitter = import_gds(splitter_path, cellname=splitter_cell, rename_duplicated_cells=True)
    add_ports_from_markers_center(splitter, pin_layer=(1, 10), port_layer=(1, 0))
    auto_rename_ports_orientation(splitter)
    splitter.remove_layers(layers=[(1, 10), (68, 0)], recursive=True)
    splitter.name = f"{splitter_cell}_splitter"

    combiner = import_gds(combiner_path, cellname=combiner_cell, rename_duplicated_cells=True)
    add_ports_from_markers_center(combiner, pin_layer=(1, 10), port_layer=(1, 0))
    auto_rename_ports_orientation(combiner)
    combiner.remove_layers(layers=[(1, 10), (68, 0)], recursive=True)
    combiner.name = f"{combiner_cell}_combiner"

    gc = import_gds(gc_path, cellname=gc_cell, rename_duplicated_cells=True)
    add_ports_from_markers_center(gc, pin_layer=(1, 10), port_layer=(1, 0))
    auto_rename_ports_orientation(gc)
    gc.remove_layers(layers=[(68, 0)], recursive=True)
    gc.name = f"{gc_cell}_gc"

    mzi = gf.components.mzi(
        splitter=splitter,
        combiner=combiner,
        cross_section=xs,
        port_e1_splitter="oE1",
        port_e0_splitter="oE0",
        port_e1_combiner="oE1",
        port_e0_combiner="oE0",
        delta_length=float(delta_length_um),
        length_x=float(length_x_um),
        length_y=float(length_y_um),
    )

    # Port indices of MZI are as follows:
    # 1        ________        3
    #   \    /          \    /
    #    ----            ----
    #    ----            ----
    #   /    \          /    \
    # 0        --------        2

    c = gf.Component()

    def _ports_list(component):
        ports = component.ports
        return list(ports.values()) if hasattr(ports, "values") else list(ports)

    def _pick_gc_port(component):
        ports = _ports_list(component)
        optical = [
            p for p in ports if getattr(p, "port_type", None) in (None, "optical")
        ]
        ports = optical or ports
        for port in ports:
            if port.orientation is not None and abs((port.orientation - 180) % 360) < 1e-3:
                return port
        return ports[0]

    mzi_ports = _ports_list(mzi)
    if hasattr(mzi.ports, "get") and all(name in mzi.ports for name in ("o1", "o2", "o3")):
        mzi_input = mzi.ports["o1"]
        mzi_out_through = mzi.ports["o2"]
        mzi_out_cross = mzi.ports["o3"]
    else:
        optical_ports = [
            p for p in mzi_ports if getattr(p, "port_type", None) in (None, "optical")
        ]
        mzi_ports = optical_ports or mzi_ports
        mzi_input = min(mzi_ports, key=lambda p: p.center[0])
        mzi_outputs = [p for p in mzi_ports if p is not mzi_input]
        mzi_outputs = sorted(mzi_outputs, key=lambda p: p.center[1])
        if len(mzi_outputs) >= 2:
            mzi_out_cross, mzi_out_through = mzi_outputs[0], mzi_outputs[-1]
        else:
            mzi_out_through = mzi_outputs[0]
            mzi_out_cross = mzi_outputs[0]

    gc_port = _pick_gc_port(gc)
    gc_port_name = gc_port.name
    if gc.ports[gc_port_name].orientation is not None:
        rotation = (180 - gc.ports[gc_port_name].orientation) % 360
        if rotation:
            gc = gf.functions.rotate(gc, rotation)

    port_names = [mzi_input.name, mzi_out_through.name, mzi_out_cross.name]
    if any(name is None for name in port_names):
        port_names = None

    c = gf.routing.add_fiber_array(
        component=mzi,
        grating_coupler=gc,
        gc_port_name=gc_port_name,
        gc_port_name_fiber=gc_port_name,
        port_names=port_names,
        pitch=127.0,
        radius=20.0,
        with_loopback=False,
        start_straight_length=0.0,
        end_straight_length=0.0,
        force_manhattan=True,
    )

    import matplotlib.pyplot as plt_layout
    fig_layout = c.plot()
    plt_layout.show()
    mo.md("### Layout preview (MZI + grating couplers)")
    return (c,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add second output port (layout)

    The solution layout exposes **two outputs** (through + cross). The snippet above
    adds a second output port and distinct port names.

    **Checklist**
    - The second port is on PinRec (1/10).
    - Port names are distinct (e.g., `o_through`, `o_cross` or similar).
    - The port orientation is correct for the output waveguide.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="layers"></a>
    ## Add submission layers

    These layers are required for openEBL checks. In this homework, we will add them for you:

    - **PinRec (1/10)** for ports
    - **DevRec (68/0)** around the device
    - **Text (10/0)** for labels
    - **Floorplan (99/0)** if required by your run
    """)
    return


@app.cell(hide_code=True)
def _(c, mo):
    mo.stop(
        c is None,
        mo.md("No layout available yet.")
    )

    # PinRec markers are provided by the grating coupler cells.

    layout_bbox = c.bbox() if callable(getattr(c, "bbox", None)) else c.bbox
    if hasattr(layout_bbox, "left"):
        xmin, ymin, xmax, ymax = (
            layout_bbox.left,
            layout_bbox.bottom,
            layout_bbox.right,
            layout_bbox.top,
        )
    else:
        (xmin, ymin), (xmax, ymax) = layout_bbox[0], layout_bbox[1]

    pad = 5.0
    c.add_polygon(
        [
            (xmin - pad, ymin - pad),
            (xmax + pad, ymin - pad),
            (xmax + pad, ymax + pad),
            (xmin - pad, ymax + pad),
        ],
        layer=(68, 0),
    )
    c.add_polygon(
        [
            (xmin - pad, ymin - pad),
            (xmax + pad, ymin - pad),
            (xmax + pad, ymax + pad),
            (xmin - pad, ymax + pad),
        ],
        layer=(99, 0),
    )

    c.add_label(text="TOP", position=(xmin, ymax + 10.0), layer=(10, 0))
    c.add_label(text="MZI", position=(xmin, ymin - 10.0), layer=(10, 0))

    mo.md("Added PinRec/DevRec/Text/Floorplan layers to the layout.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simphony spectrum (solution)

    Use Simphony + SAX to build an MZI circuit model and plot spectra.

    **Requirements**
    1. Use SiEPIC compact models (`simphony.libraries.siepic`).
    2. Plot **one output port** that matches the starter layout (single output).
    3. After you add a second output port to your layout GDS, plot **both outputs** (through + cross).
    4. Sweep wavelength near 1550 nm (e.g., 1.53–1.57 µm).
    """)
    return


@app.cell
def _(delta_length_um):
    import numpy as np
    import matplotlib.pyplot as plt_sim
    import sax
    from simphony.libraries import siepic

    wl = np.linspace(1.53, 1.57, 401)
    base_length_um = 2000.0

    mzi_circuit, _ = sax.circuit(
        netlist={
            "instances": {
                "splitter": "y_branch",
                "short_wg": "waveguide",
                "long_wg": "waveguide",
                "combiner": "directional_coupler",
            },
            "connections": {
                "splitter,port_2": "short_wg,o0",
                "splitter,port_3": "long_wg,o0",
                "short_wg,o1": "combiner,port_1",
                "long_wg,o1": "combiner,port_2",
            },
            "ports": {
                "input": "splitter,port_1",
                "through": "combiner,port_3",
                "cross": "combiner,port_4",
            },
        },
        models={
            "y_branch": siepic.y_branch,
            "directional_coupler": siepic.directional_coupler,
            "waveguide": siepic.waveguide,
        },
    )

    sim_kwargs = {
        "wl": wl,
        "short_wg": {
            "length": base_length_um,
            "pol": "te",
            "width": 500.0,
            "height": 220.0,
            "loss": 0.0,
        },
        "long_wg": {
            "length": base_length_um + float(delta_length_um),
            "pol": "te",
            "width": 500.0,
            "height": 220.0,
            "loss": 0.0,
        },
    }

    S = mzi_circuit(**sim_kwargs)
    through = np.abs(S["through", "input"]) ** 2
    cross = np.abs(S["cross", "input"]) ** 2

    fig_sim, ax = plt_sim.subplots()
    ax.plot(wl * 1e3, through, label="Through")
    ax.plot(wl * 1e3, cross, label="Cross")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Transmission (a.u.)")
    ax.set_title("MZI spectrum (Simphony/SAX)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt_sim.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="export"></a>
    ## Export for submission

    Run this cell to export the final GDS to your openEBL submissions folder.
    """)
    return


@app.cell(hide_code=True)
def _(c, export_gds, mo):
    mo.stop(
        c is None,
        mo.md("No layout available yet.")
    )
    import pathlib
    import subprocess

    out = pathlib.Path(str(export_gds)).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    written = c.write_gds(out)
    script = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "run_klayout_drc.sh"
    report = out.with_suffix(".lyrdb")
    if script.exists():
        try:
            subprocess.run(
                [str(script), str(out), str(report)],
                check=True,
            )
            mo.md(f"Wrote: `{written}`\n\nDRC report: `{report}`")
        except subprocess.CalledProcessError as exc:
            mo.md(f"Wrote: `{written}`\n\nDRC failed: `{exc}`")
    else:
        mo.md(f"Wrote: `{written}`\n\nDRC script not found: `{script}`")
    return


if __name__ == "__main__":
    app.run()
