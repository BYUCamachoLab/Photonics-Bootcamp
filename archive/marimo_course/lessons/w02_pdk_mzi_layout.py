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
        options=("All", "Overview", "Build MZI + Targets", "Layout skeleton", "Submission"),
        value="All",
    )
    section_tabs
    return set_view, view_state


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_targets = view in ["All", "Build MZI + Targets"]
    show_skeleton = view in ["All", "Layout skeleton"]
    show_submission = view in ["All", "Submission"]
    return show_overview, show_skeleton, show_submission, show_targets, view


@app.cell
def _(doc_badges, view):
    doc_badges(
        [
            f"Notebook view: <strong>{view}</strong>",
        ]
    )
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    from _style import header

    header(
        mo,
        title="PDK MZI layout (SiEPIC PDK)",
        subtitle=(
            "Build a first MZI layout using the SiEPIC-EBeam PDK workflow in Python. "
            "Use modelling targets (ΔL ↔ FSR) to guide geometry choices, then save your work in the openEBL repo."
        ),
        badges=["Week 2", "Lab companion", "PDK", "openEBL workflow"],
        toc=[
            ("Overview", "overview"),
            ("Build MZI + Targets", "targets"),
            ("Layout skeleton", "skeleton"),
            ("Submission", "submission"),
        ],
        build="2025-12-16",
    )
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    overview_md = mo.md(r"""
    <a id="overview"></a>
    ## Overview

    This is the **PDK + compact-model + layout** companion for Week 2. The modelling companion is:
    `marimo_course/lessons/w02_mzi_modelling.py`, where you derived and explored the ideal MZI transfer function.

    In this notebook, you'll connect three ideas that show up in every photonics workflow:

    - **Compact models:** fast, circuit-level models of components (couplers, waveguides, phase shifters) that let you
      simulate a whole photonic circuit without solving Maxwell's equations everywhere.
    - **PDK (process design kit):** a foundry/technology "package" that defines the **design rules**, **layers**, and
      **parameterized building blocks** (plus their compact models) so your design is manufacturable and checkable.
    - **Reproducibility across views:** build the *same* MZI you modelled last lesson, first as a **circuit** from compact
      models and then as a **layout** using PDK cells.

    In lab, you will:

    1. Build an MZI from **compact models** (component → circuit) and sanity-check it against the Week 2 model.
    2. Decide on a **target** (FSR → ΔL) near **1550 nm**.
    3. Assemble the same MZI from **PDK building blocks** (splitter, waveguides, combiner, I/O).
    4. Add the **conventions** required for downstream checks (ports/pins, DevRec, labels/floorplan as required).
    5. Save your design in the **openEBL** submission repo and keep CI green.
    """)

    goals = doc_callout_list(
        "info",
        tag="Learning goals",
        title="What you should be able to do after this notebook",
        items=[
            "Explain what a compact model is and why we use them for circuit-level photonics design.",
            "Describe what a PDK provides (layers, rules, cells, models) and why it matters for manufacturable layouts.",
            "Create an MZI from compact-model building blocks and connect ΔL ↔ FSR back to the modelling notebook.",
            "Implement the same MZI using PDK-accurate cells so it passes downstream checks.",
        ],
    )

    grading_note = doc_callout_list(
        "warning",
        tag="Where is the graded work?",
        title="Lab companion vs homework",
        items=[
            "This notebook is a lab companion (workflow + checklists + reference).",
            "Graded work should live in a homework notebook under `marimo_course/assignments/`.",
        ],
    )
    mo.vstack([overview_md, goals, grading_note])
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    placed_blocks = mo.ui.checkbox(label="Placed I/O + splitter/combiner cells", value=False)
    routed = mo.ui.checkbox(label="Routed an MZI skeleton with ΔL", value=False)
    annotated = mo.ui.checkbox(label="Added pins/DevRec/labels as required", value=False)
    saved = mo.ui.checkbox(label="Saved in openEBL repo + CI checked", value=False)
    mo.vstack([placed_blocks, routed, annotated, saved])
    return


@app.cell
def _(mo, set_view, show_overview):
    mo.stop(not show_overview)
    go_targets = mo.ui.button(
        value=0,
        kind="success",
        label="Go to Build MZI + Targets",
        on_click=lambda v: (set_view("Build MZI + Targets"), (v or 0) + 1)[-1],
    )
    go_skeleton = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to Layout skeleton",
        on_click=lambda v: (set_view("Layout skeleton"), (v or 0) + 1)[-1],
    )
    go_submission = mo.ui.button(
        value=0,
        kind="neutral",
        label="Go to Submission",
        on_click=lambda v: (set_view("Submission"), (v or 0) + 1)[-1],
    )
    mo.hstack([go_targets, go_skeleton, go_submission], justify="start", gap=1)
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    mo.md(r"""
    <a id="targets"></a>
    ## Build the MZI + targets

    Build the MZI from PDK components, render the layout, and then pick a ΔL that
    matches your target FSR near 1550 nm.
    """)
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    import textwrap

    layout_code = textwrap.dedent(
        """
        ```python
        # Build MZI, add pins/DevRec/labels/floorplan, and export a GDS.
        from pathlib import Path
        import gdsfactory as gf
        from gdsfactory.add_ports import add_ports_from_markers_center
        from gdsfactory.read import import_gds
        from gdsfactory.port import auto_rename_ports_orientation

        if hasattr(gf, "gpdk") and hasattr(gf.gpdk, "PDK"):
            gf.gpdk.PDK.activate()

        # 1) Define the waveguide cross-section used for routing the MZI arms.
        xs = gf.cross_section.strip(layer=(1, 0), width=0.5)
        pdk_gds = Path(
            "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_bdc_te1550.gds"
        )
        # 2) Load the splitter PDK cell from the SiEPIC GDS and add ports from PinRec.
        splitter = import_gds(pdk_gds, cellname="ebeam_bdc_te1550")
        add_ports_from_markers_center(splitter, pin_layer=(1, 10), port_layer=(1, 0))
        auto_rename_ports_orientation(splitter)

        # 3) Build the MZI by connecting two splitters with routed waveguide arms.
        mzi = gf.components.mzi(
            splitter=splitter,
            combiner=splitter,
            cross_section=xs,
            port_e1_splitter="oE1",
            port_e0_splitter="oE0",
            port_e1_combiner="oE1",
            port_e0_combiner="oE0",
            delta_length=50.0,
            length_x=60.0,
            length_y=10.0,
        )

        gc_gds = Path(
            "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_gc_te1550.gds"
        )
        # 4) Load the grating coupler cell and add ports so we can connect to I/O.
        gc = import_gds(gc_gds, cellname="ebeam_gc_te1550")
        add_ports_from_markers_center(gc, pin_layer=(1, 10), port_layer=(1, 0))
        auto_rename_ports_orientation(gc)

        def pick_port(component, orientation, *, fallback_first=False):
            ports = component.ports
            port_list = list(ports.values()) if hasattr(ports, "values") else list(ports)
            for port in port_list:
                if port.orientation is not None and int(round(port.orientation)) == orientation:
                    return port
            if fallback_first and port_list:
                return port_list[0]
            raise ValueError(f"No port with orientation {orientation} on {component.name}")

        # 5) Assemble the final layout by connecting two GCs to the MZI I/O ports.
        c = gf.Component()
        mzi_ref = c << mzi
        mzi_in = pick_port(mzi_ref, 180)
        mzi_out = pick_port(mzi_ref, 0)
        gc_port = pick_port(gc, 180, fallback_first=True)
        gc_in = c << gc
        gc_in.connect(gc_port.name, mzi_in)
        gc_out = c << gc
        gc_out.connect(gc_port.name, mzi_out)

        # 6) Add PinRec markers on each external port (required by openEBL).
        pin_layer = (1, 10)
        pin_w = 2.0
        pin_h = 1.0
        for port in c.ports.values():
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

        # 7) Add DevRec and Floorplan boxes around the full layout bbox.
        xmin, ymin = c.bbox[0]
        xmax, ymax = c.bbox[1]
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

        # 8) Add Text labels for top cell and measurement tags.
        c.add_label(text="TOP", position=(xmin, ymax + 10.0), layer=(10, 0))
        c.add_label(text="MZI", position=(xmin, ymin - 10.0), layer=(10, 0))

        # 9) Export a submission-ready GDS to the openEBL submissions folder.
        out = Path("openEBL-2026-02/submissions/EBeam_username.gds")
        out.parent.mkdir(parents=True, exist_ok=True)
        c.write_gds(out)
        ```
        """
    ).strip()
    mo.md(layout_code)
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)

    from _notebook_template import optional_import as optional_import_preview

    gf_preview = None
    gf_preview, gf_preview_error = optional_import_preview("gdsfactory")
    preview_output = None
    if gf_preview is None:
        preview_notice = [mo.md("Layout preview: `gdsfactory` is not available in this environment.")]
        if gf_preview_error:
            preview_notice.append(mo.md(f"Details: `{gf_preview_error}`"))
        preview_output = mo.vstack(preview_notice)
    else:
        try:
            import pathlib as pathlib_preview
            from gdsfactory.add_ports import add_ports_from_markers_center
            from gdsfactory.read import import_gds
            from gdsfactory.port import auto_rename_ports_orientation

            if hasattr(gf_preview, "gpdk") and hasattr(gf_preview.gpdk, "PDK"):
                gf_preview.gpdk.PDK.activate()

            # Build the MZI layout from PDK cells and prepare a preview image.
            xs = gf_preview.cross_section.strip(layer=(1, 0), width=0.5)
            pdk_gds = pathlib_preview.Path(
                "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_bdc_te1550.gds"
            )
            if not pdk_gds.exists():
                raise FileNotFoundError(f"SiEPIC PDK GDS not found at {pdk_gds}")

            splitter = import_gds(pdk_gds, cellname="ebeam_bdc_te1550")
            add_ports_from_markers_center(splitter, pin_layer=(1, 10), port_layer=(1, 0))
            auto_rename_ports_orientation(splitter)

            # Route the MZI using the SiEPIC splitter for both couplers.
            mzi = gf_preview.components.mzi(
                splitter=splitter,
                combiner=splitter,
                cross_section=xs,
                port_e1_splitter="oE1",
                port_e0_splitter="oE0",
                port_e1_combiner="oE1",
                port_e0_combiner="oE0",
                delta_length=50.0,
                length_x=60.0,
                length_y=10.0,
            )

            gc_gds = pathlib_preview.Path(
                "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_gc_te1550.gds"
            )
            if not gc_gds.exists():
                raise FileNotFoundError(f"SiEPIC PDK GDS not found at {gc_gds}")
            gc = import_gds(gc_gds, cellname="ebeam_gc_te1550")
            add_ports_from_markers_center(gc, pin_layer=(1, 10), port_layer=(1, 0))
            auto_rename_ports_orientation(gc)

            # Attach grating couplers to the MZI input and output.
            def pick_port(component, orientation, *, fallback_first=False):
                ports = component.ports
                port_list = list(ports.values()) if hasattr(ports, "values") else list(ports)
                for port in port_list:
                    if port.orientation is not None and int(round(port.orientation)) == orientation:
                        return port
                if fallback_first and port_list:
                    return port_list[0]
                raise ValueError(f"No port with orientation {orientation} on {component.name}")

            c = gf_preview.Component()
            mzi_ref = c << mzi
            mzi_in = pick_port(mzi_ref, 180)
            mzi_out = pick_port(mzi_ref, 0)
            gc_port = pick_port(gc, 180, fallback_first=True)
            gc_in = c << gc
            gc_in.connect(gc_port.name, mzi_in)
            gc_out = c << gc
            gc_out.connect(gc_port.name, mzi_out)

            # Render the layout as a PNG for display in the notebook.
            fig = c.plot()
            if fig is None:
                import matplotlib.pyplot as plt
                fig = plt.gcf()
            from io import BytesIO

            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            preview_output = mo.vstack(
                [
                    mo.md("### Final rendering (complete MZI cell)"),
                    mo.image(buf),
                ]
            )
        except Exception as e:  # pragma: no cover
            preview_output = mo.md(f"(Could not build preview: `{type(e).__name__}: {e}`)")
    preview_output
    return


@app.cell
def _(doc_callout_html, mo, show_targets):
    mo.stop(not show_targets)
    mo.md(r"""
    ### Targets: pick ΔL from an FSR target (1550 nm default)

    Use the Week 2 modelling notebook to build intuition and sanity-check values:
    `marimo_course/lessons/w02_mzi_modelling.py`.

    Rule-of-thumb near λ0:

    $$
    \mathrm{FSR} \approx \frac{\lambda_0^2}{n_g\,\Delta L}.
    $$
    """)

    doc_callout_html(
        "info",
        tag="Tip",
        title="What matters for FSR",
        html=(
            "- ΔL sets fringe spacing (FSR) approximately as `1/ΔL`.\n"
            "- Base length doesn’t change FSR in the ideal model.\n"
            "- Use **1550 nm** by default; treat **1310 nm** as an extension."
        ),
    )
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    wl0_nm = mo.ui.number(value=1550.0, label="λ0 (nm)")
    ng = mo.ui.number(value=4.19, label="ng (group index)")
    deltaL_um = mo.ui.number(value=50.0, label="Planned ΔL (µm)")
    mo.hstack([wl0_nm, ng, deltaL_um])
    return deltaL_um, ng, wl0_nm


@app.cell
def _(deltaL_um, mo, ng, show_targets, wl0_nm):
    mo.stop(not show_targets)
    wl0_um = float(wl0_nm.value) / 1e3
    ng_val = float(ng.value)
    delta_L_um = float(deltaL_um.value)
    fsr_nm = (
        None
        if (delta_L_um <= 0 or ng_val <= 0)
        else (wl0_um * wl0_um) / (ng_val * delta_L_um) * 1e3
    )
    mo.md(
        "FSR estimate: (enter positive ΔL and ng)"
        if fsr_nm is None
        else f"FSR estimate: **{fsr_nm:.2f} nm**"
    )
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    mo.md(r"""
    ### Notebook version of the openEBL pre-submission steps

    These mirror the typical PDK workflow, but are implemented directly in Python.
    Use the toggles below to add required layers before exporting a GDS.
    """)
    return


@app.cell
def _(mo, show_targets):
    mo.stop(not show_targets)
    add_pins = mo.ui.checkbox(label="Add PinRec markers (1/10)", value=True)
    add_devrec = mo.ui.checkbox(label="Add DevRec box (68/0)", value=True)
    add_floorplan = mo.ui.checkbox(label="Add Floorplan box (99/0)", value=False)
    add_labels = mo.ui.checkbox(label="Add Text labels (10/0)", value=True)
    export_path = mo.ui.text(
        value="openEBL-2026-02/submissions/EBeam_username.gds",
        label="Export path",
    )
    mo.vstack(
        [
            mo.hstack([add_pins, add_devrec, add_floorplan, add_labels]),
            export_path,
        ]
    )
    return add_devrec, add_floorplan, add_labels, add_pins, export_path


@app.cell
def _(
    add_devrec,
    add_floorplan,
    add_labels,
    add_pins,
    export_path,
    mo,
    show_targets,
):
    mo.stop(not show_targets)

    from _notebook_template import optional_import as optional_import_export

    gf_export = None
    gf_export, gf_export_error = optional_import_export("gdsfactory")
    build_export_output = None
    if gf_export is None:
        export_notice = [mo.md("Build/export: `gdsfactory` is not available in this environment.")]
        if gf_export_error:
            export_notice.append(mo.md(f"Details: `{gf_export_error}`"))
        build_export_output = mo.vstack(export_notice)
    else:
        try:
            import pathlib as pathlib_export
            from gdsfactory.add_ports import add_ports_from_markers_center as add_ports_export
            from gdsfactory.read import import_gds as import_gds_export
            from gdsfactory.port import auto_rename_ports_orientation as rename_ports_export

            if hasattr(gf_export, "gpdk") and hasattr(gf_export.gpdk, "PDK"):
                gf_export.gpdk.PDK.activate()

            # Build the base MZI layout (same as preview) and then add submission layers.
            xs_export = gf_export.cross_section.strip(layer=(1, 0), width=0.5)
            pdk_gds_export = pathlib_export.Path(
                "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_bdc_te1550.gds"
            )
            if not pdk_gds_export.exists():
                build_export_output = mo.md(
                    f"(Build/export failed: SiEPIC splitter GDS not found at `{pdk_gds_export}`)"
                )
            else:
                # Load the splitter cell from the PDK and make sure ports are available.
                splitter_export = import_gds_export(
                    pdk_gds_export,
                    cellname="ebeam_bdc_te1550",
                    rename_duplicated_cells=True,
                )
                add_ports_export(splitter_export, pin_layer=(1, 10), port_layer=(1, 0))
                rename_ports_export(splitter_export)
                splitter_export.name = "ebeam_bdc_te1550_splitter"

                mzi_export = gf_export.components.mzi(
                    splitter=splitter_export,
                    combiner=splitter_export,
                    cross_section=xs_export,
                    port_e1_splitter="oE1",
                    port_e0_splitter="oE0",
                    port_e1_combiner="oE1",
                    port_e0_combiner="oE0",
                    delta_length=50.0,
                    length_x=60.0,
                    length_y=10.0,
                )

                gc_gds_export = pathlib_export.Path(
                    "SiEPIC_EBeam_PDK_public/klayout/EBeam/gds/EBeam/ebeam_gc_te1550.gds"
                )
                if not gc_gds_export.exists():
                    build_export_output = mo.md(
                        f"(Build/export failed: SiEPIC GC GDS not found at `{gc_gds_export}`)"
                    )
                else:
                    # Load the grating coupler cell for I/O.
                    gc_export = import_gds_export(
                        gc_gds_export,
                        cellname="ebeam_gc_te1550",
                        rename_duplicated_cells=True,
                    )
                    add_ports_export(gc_export, pin_layer=(1, 10), port_layer=(1, 0))
                    rename_ports_export(gc_export)
                    gc_export.name = "ebeam_gc_te1550_gc"

                    def pick_port_export(component, orientation, *, fallback_first=False):
                        ports = component.ports
                        port_list = (
                            list(ports.values()) if hasattr(ports, "values") else list(ports)
                        )
                        for port in port_list:
                            if port.orientation is not None and int(round(port.orientation)) == orientation:
                                return port
                        if fallback_first and port_list:
                            return port_list[0]
                        raise ValueError(
                            f"No port with orientation {orientation} on {component.name}"
                        )

                    # Assemble the final layout by connecting GCs to the MZI ports.
                    c_export = gf_export.Component()
                    mzi_ref_export = c_export << mzi_export
                    mzi_in_export = pick_port_export(mzi_ref_export, 180)
                    mzi_out_export = pick_port_export(mzi_ref_export, 0)
                    gc_port_export = pick_port_export(gc_export, 180, fallback_first=True)
                    gc_in_export = c_export << gc_export
                    gc_in_export.connect(gc_port_export.name, mzi_in_export)
                    gc_out_export = c_export << gc_export
                    gc_out_export.connect(gc_port_export.name, mzi_out_export)

                    # Add PinRec markers for all external ports (required for openEBL).
                    if add_pins.value:
                        pin_layer = (1, 10)
                        pin_w = 2.0
                        pin_h = 1.0
                        ports = c_export.ports
                        port_list = (
                            list(ports.values()) if hasattr(ports, "values") else list(ports)
                        )
                        for port in port_list:
                            cx, cy = port.center
                            c_export.add_polygon(
                                [
                                    (cx - pin_w / 2, cy - pin_h / 2),
                                    (cx + pin_w / 2, cy - pin_h / 2),
                                    (cx + pin_w / 2, cy + pin_h / 2),
                                    (cx - pin_w / 2, cy + pin_h / 2),
                                ],
                                layer=pin_layer,
                            )

                    def get_bbox(component):
                        bbox = component.bbox() if callable(getattr(component, "bbox", None)) else component.bbox
                        if hasattr(bbox, "left"):
                            return bbox.left, bbox.bottom, bbox.right, bbox.top
                        if hasattr(bbox, "__getitem__"):
                            (xmin, ymin), (xmax, ymax) = bbox[0], bbox[1]
                            return xmin, ymin, xmax, ymax
                        raise TypeError("Unsupported bbox type")

                    # Add DevRec and optional Floorplan around the layout bbox.
                    if add_devrec.value or add_floorplan.value:
                        xmin, ymin, xmax, ymax = get_bbox(c_export)
                        pad = 5.0
                        if add_devrec.value:
                            c_export.add_polygon(
                                [
                                    (xmin - pad, ymin - pad),
                                    (xmax + pad, ymin - pad),
                                    (xmax + pad, ymax + pad),
                                    (xmin - pad, ymax + pad),
                                ],
                                layer=(68, 0),
                            )
                        if add_floorplan.value:
                            c_export.add_polygon(
                                [
                                    (xmin - pad, ymin - pad),
                                    (xmax + pad, ymin - pad),
                                    (xmax + pad, ymax + pad),
                                    (xmin - pad, ymax + pad),
                                ],
                                layer=(99, 0),
                            )

                    # Add Text labels for top-cell naming and identification.
                    if add_labels.value:
                        xmin, ymin, xmax, ymax = get_bbox(c_export)
                        c_export.add_label(
                            text="TOP",
                            position=(xmin, ymax + 10.0),
                            layer=(10, 0),
                        )
                        c_export.add_label(
                            text="MZI",
                            position=(xmin, ymin - 10.0),
                            layer=(10, 0),
                        )

                    # Export the final GDS to the openEBL submissions folder.
                    out_export = pathlib_export.Path(str(export_path.value)).expanduser()
                    out_export.parent.mkdir(parents=True, exist_ok=True)
                    written_export = c_export.write_gds(out_export)
                    build_export_output = mo.vstack(
                        [
                            mo.md(f"Wrote: `{written_export}`"),
                            mo.md(
                                "Reminder: verify the top-cell name and port labels in your layout viewer."
                            ),
                        ]
                    )
        except Exception as e:  # pragma: no cover
            build_export_output = mo.md(f"(Build/export failed: `{type(e).__name__}: {e}`)")
    build_export_output
    return


@app.cell
def _(mo, show_skeleton):
    mo.stop(not show_skeleton)
    enable_gdsfactory = mo.ui.checkbox(
        label="Enable gdsfactory helper (may take a while to import)",
        value=False,
    )
    enable_gdsfactory
    return (enable_gdsfactory,)


@app.cell
def _(enable_gdsfactory, mo, show_skeleton):
    mo.stop(not show_skeleton)
    from _notebook_template import optional_import as optional_import_skeleton

    gf_mod = None
    available = False
    if not enable_gdsfactory.value:
        msg = mo.md(
            "Optional gdsfactory helper: **disabled** (enable the checkbox to import)"
        )
    else:
        gf_mod, gf_error = optional_import_skeleton("gdsfactory")
        available = gf_mod is not None
        msg = mo.md(
            "Optional gdsfactory helper: **available**"
            if available
            else f"Optional gdsfactory helper: **not available** (`{gf_error}`)"
        )
    msg
    return available, gf_mod


@app.cell
def _(available, mo, show_skeleton):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    # Parameters for a quick, generic MZI skeleton export.
    gds_out = mo.ui.text(value="marimo_course/build/week2_mzi_skeleton.gds", label="GDS output path")
    delta_length = mo.ui.number(value=50.0, label="ΔL (µm)")
    length_x = mo.ui.number(value=60.0, label="length_x (µm)")
    length_y = mo.ui.number(value=10.0, label="length_y (µm)")
    write = mo.ui.button(value=0, label="Write GDS", kind="success", on_click=lambda v: (v or 0) + 1)
    mo.vstack([mo.hstack([gds_out, write]), mo.hstack([delta_length, length_x, length_y])])
    return delta_length, gds_out, length_x, length_y, write


@app.cell
def _(available, gf_mod, mo, show_skeleton):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    from pathlib import Path

    def write_mzi_skeleton(*, out: Path, delta_length_um: float, length_x_um: float, length_y_um: float) -> Path:
        gf = gf_mod
        # Create a generic MZI to visualize geometry only (not PDK-accurate).
        mzi = gf.components.mzi(
            delta_length=float(delta_length_um),
            length_x=float(length_x_um),
            length_y=float(length_y_um),
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        written = mzi.write_gds(gdspath=out)
        return Path(written)
    return Path, write_mzi_skeleton


@app.cell
def _(
    Path,
    available,
    delta_length,
    gds_out,
    length_x,
    length_y,
    mo,
    show_skeleton,
    write,
    write_mzi_skeleton,
):
    mo.stop(not show_skeleton)
    mo.stop(not available)

    blocks = []
    if int(write.value or 0) <= 0:
        blocks.append(
            mo.md("Click **Write GDS** to export a skeleton you can inspect in a layout viewer.")
        )
    else:
        out = Path(str(gds_out.value)).expanduser()
        try:
            # Write the skeleton GDS file and report the path.
            written = write_mzi_skeleton(
                out=out,
                delta_length_um=float(delta_length.value),
                length_x_um=float(length_x.value),
                length_y_um=float(length_y.value),
            )
            blocks.append(mo.md(f"Wrote: `{written}`"))
            blocks.append(mo.md(f"Open in your layout viewer: `{written}`"))
        except Exception as e:  # pragma: no cover
            blocks.append(mo.md(f"(GDS write failed: `{type(e).__name__}: {e}`)"))

    mo.vstack(blocks)
    return


@app.cell
def _(doc_callout_list, mo, show_submission):
    mo.stop(not show_submission)
    mo.md(r"""
    <a id="submission"></a>
    ## Save + submission workflow (openEBL)

    The details depend on the specific openEBL run repository used this semester, but the structure is consistent:
    save designs in the right folder, run checks, fix failures, and submit via PR.
    """)

    doc_callout_list(
        "info",
        tag="Checklist",
        title="Before you push",
        ordered=True,
        items=[
            "Confirm your layout file is inside the run repo (e.g., `openEBL-2026-02/submissions/...`).",
            "Verify naming conventions and top-level cell structure match the run instructions.",
            "Run local verification in your layout viewer if available.",
            "Push to your fork and check GitHub Actions results; download artifacts when something fails.",
        ],
    )
    return


if __name__ == "__main__":
    app.run()
