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

__generated_with = "0.19.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from _assignment_template import load_lesson_template, _ensure_lessons_on_path

    _ensure_lessons_on_path()
    from _notebook_template import optional_import

    inject_css, make_doc_helpers, make_health_refresh_button, header = load_lesson_template()
    return header, inject_css, make_doc_helpers, optional_import


@app.cell
def _(inject_css, mo):
    inject_css(mo)
    return


@app.cell
def _(make_doc_helpers, mo):
    doc_badges, doc_callout_html, doc_callout_list = make_doc_helpers(mo)
    return (doc_callout_list,)


@app.cell
def _(header, mo):
    header(
        mo,
        title="HW02 — MZI layout + openEBL prep",
        subtitle=(
            "Build a student-owned MZI layout in Python using the SiEPIC-EBeam PDK cells, "
            "then add PinRec/DevRec/labels and export a submission-ready GDS."
        ),
        badges=["Week 2", "Homework", "PDK layout", "openEBL prep"],
        toc=[
            ("Overview", "overview"),
            ("Build MZI", "build"),
            ("Add Submission Layers", "layers"),
            ("Export", "export"),
        ],
        build="2025-12-16",
    )
    return


@app.cell
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

    doc_callout_list(
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
    return (overview_md,)


@app.cell
def _(overview_md):
    overview_md
    return


@app.cell
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


@app.cell
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
    mo.md("**EDIT HERE — set your MZI parameters**")
    # === EDIT THIS CELL ===
    username = "username"

    delta_length_um = 300.0
    length_x_um = 60.0
    length_y_um = 10.0

    splitter_gds = (
        "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_bdc_te1550.gds"
    )
    splitter_cell = "ebeam_bdc_te1550"

    gc_gds = "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_gc_te1550.gds"
    gc_cell = "ebeam_gc_te1550"

    export_gds = f"openEBL-2026-02/submissions/EBeam_{username}.gds"

    mo.md(
        "\n".join(
            [
                f"- ΔL: `{delta_length_um}` µm",
                f"- length_x: `{length_x_um}` µm",
                f"- length_y: `{length_y_um}` µm",
                f"- splitter cell: `{splitter_cell}`",
                f"- GC cell: `{gc_cell}`",
                f"- export path: `{export_gds}`",
            ]
        )
    )
    return (
        delta_length_um,
        export_gds,
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
    gc_cell,
    gc_gds,
    length_x_um,
    length_y_um,
    mo,
    optional_import,
    splitter_cell,
    splitter_gds,
):
    gf_mod = None
    gf_mod, gf_error = optional_import("gdsfactory")
    c = None
    preview = None
    if gf_mod is None:
        preview = mo.md(f"`gdsfactory` not available: `{gf_error}`")
    else:
        import pathlib as pathlib_hw
        from io import BytesIO
        from gdsfactory.add_ports import add_ports_from_markers_center
        from gdsfactory.read import import_gds
        from gdsfactory.port import auto_rename_ports_orientation

        if hasattr(gf_mod, "gpdk") and hasattr(gf_mod.gpdk, "PDK"):
            gf_mod.gpdk.PDK.activate()

        xs = gf_mod.cross_section.strip(layer=(1, 0), width=0.5)

        splitter_path = pathlib_hw.Path(splitter_gds)
        gc_path = pathlib_hw.Path(gc_gds)
        if not splitter_path.exists():
            preview = mo.md(f"(Splitter GDS not found: `{splitter_path}`)")
        elif not gc_path.exists():
            preview = mo.md(f"(GC GDS not found: `{gc_path}`)")
        else:
            splitter = import_gds(
                splitter_path, cellname=splitter_cell, rename_duplicated_cells=True
            )
            add_ports_from_markers_center(splitter, pin_layer=(1, 10), port_layer=(1, 0))
            auto_rename_ports_orientation(splitter)
            splitter.name = f"{splitter_cell}_splitter"

            gc = import_gds(gc_path, cellname=gc_cell, rename_duplicated_cells=True)
            add_ports_from_markers_center(gc, pin_layer=(1, 10), port_layer=(1, 0))
            auto_rename_ports_orientation(gc)
            gc.name = f"{gc_cell}_gc"

            mzi = gf_mod.components.mzi(
                splitter=splitter,
                combiner=splitter,
                cross_section=xs,
                port_e1_splitter="oE1",
                port_e0_splitter="oE0",
                port_e1_combiner="oE1",
                port_e0_combiner="oE0",
                delta_length=float(delta_length_um),
                length_x=float(length_x_um),
                length_y=float(length_y_um),
            )

            def pick_port(component, orientation, *, fallback_first=False):
                ports = component.ports
                port_list = (
                    list(ports.values()) if hasattr(ports, "values") else list(ports)
                )
                for port in port_list:
                    if port.orientation is not None and int(round(port.orientation)) == orientation:
                        return port
                if fallback_first and port_list:
                    return port_list[0]
                raise ValueError(f"No port with orientation {orientation} on {component.name}")

            c = gf_mod.Component()
            mzi_ref = c << mzi
            mzi_in = pick_port(mzi_ref, 180)
            mzi_out = pick_port(mzi_ref, 0)
            gc_port = pick_port(gc, 180, fallback_first=True)
            gc_in = c << gc
            gc_in.connect(gc_port.name, mzi_in)
            gc_out = c << gc
            gc_out.connect(gc_port.name, mzi_out)

            fig = c.plot()
            if fig is None:
                import matplotlib.pyplot as plt
                fig = plt.gcf()
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            preview = mo.vstack(
                [
                    mo.md("### Layout preview (MZI + grating couplers)"),
                    mo.image(buf),
                ]
            )
    preview
    return (c,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Add second output port (layout)

    Your initial layout only exposes **one output**. Before submission, add a second
    output port to the GDS (cross port) so your layout has both through + cross outputs.

    **Checklist**
    - The second port is on PinRec (1/10).
    - Port names are distinct (e.g., `o_through`, `o_cross` or similar).
    - The port orientation is correct for the output waveguide.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="layers"></a>
    ## Add submission layers

    These layers are required for openEBL checks. In this homework, add them in Python:

    - **PinRec (1/10)** for ports
    - **DevRec (68/0)** around the device
    - **Text (10/0)** for labels
    - **Floorplan (99/0)** if required by your run
    """)
    return


@app.cell
def _(c, mo):
    layers_output = None
    if c is None:
        layers_output = mo.md("(No layout available yet.)")
    else:
        pin_layer = (1, 10)
        pin_w = 2.0
        pin_h = 1.0
        ports = c.ports
        port_list = list(ports.values()) if hasattr(ports, "values") else list(ports)
        for port in port_list:
            cx, cy = port.center
            c.add_polygon(
                [
                    (cx - pin_w / 2, cy - pin_h / 2),
                    (cx + pin_w / 2, cy - pin_h / 2),
                    (cx + pin_w / 2, cy + pin_h / 2),
                    (cx - pin_w / 2, cy + pin_h / 2),
                ],
                layer=pin_layer,
            )

        bbox = c.bbox() if callable(getattr(c, "bbox", None)) else c.bbox
        if hasattr(bbox, "left"):
            xmin, ymin, xmax, ymax = bbox.left, bbox.bottom, bbox.right, bbox.top
        else:
            (xmin, ymin), (xmax, ymax) = bbox[0], bbox[1]

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
        layers_output = mo.md("Added PinRec/DevRec/Text/Floorplan layers to the layout.")
    layers_output
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Simphony spectrum (blank cell — student work)

    Use Simphony + SAX to build an MZI circuit model and plot spectra.
    Leave your code in this cell for grading.

    **Requirements**
    1. Use SiEPIC compact models (`simphony.libraries.siepic`).
    2. Plot **one output port** that matches the starter layout (single output).
    3. After you add a second output port to your layout GDS, plot **both outputs** (through + cross).
    4. Sweep wavelength near 1550 nm (e.g., 1.53–1.57 µm).
    """)
    return


@app.cell
def _(mo):
    # === STUDENT: WRITE YOUR SIMPHONY/SAX CODE HERE ===
    # Example imports (uncomment as needed):
    # import numpy as np
    # import sax
    # from simphony.libraries import siepic
    #
    # Your task:
    # 1) Define a netlist (splitter -> two arms -> combiner).
    # 2) Build the circuit with sax.circuit.
    # 3) Plot the single output (through) that matches the starter layout.
    # 4) After adding a second output to your layout, plot both through + cross.
    pass


@app.cell
def _(c, export_gds, mo):
    mo.md(r"""
    <a id="export"></a>
    ## Export for submission

    Export the final GDS to your openEBL submissions folder.
    """)
    export_output = None
    if c is None:
        export_output = mo.md("(No layout available yet.)")
    else:
        import pathlib

        out = pathlib.Path(str(export_gds)).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        written = c.write_gds(out)
        export_output = mo.md(f"Wrote: `{written}`")
    export_output
    return


if __name__ == "__main__":
    app.run()
