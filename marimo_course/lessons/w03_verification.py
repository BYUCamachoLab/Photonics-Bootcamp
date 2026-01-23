#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.17.0",
#   "numpy",
#   "gdsfactory",
#   "matplotlib",
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
        options=(
            "All",
            "Overview",
            "Checklist",
            "DFT Calculator",
            "DRC Runner",
            "Layout Demo",
            "Exercises",
            "KLayout",
        ),
        value="All",
    )
    section_tabs
    return set_view, view_state


@app.cell
def _(view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_checklist = view in ["All", "Checklist"]
    show_dft = view in ["All", "DFT Calculator"]
    show_drc = view in ["All", "DRC Runner"]
    show_layout = view in ["All", "Layout Demo"]
    show_exercises = view in ["All", "Exercises"]
    show_klayout = view in ["All", "KLayout"]
    return (
        show_checklist,
        show_dft,
        show_drc,
        show_exercises,
        show_klayout,
        show_layout,
        show_overview,
        view,
    )


@app.cell
def _(mo):
    # Shared "active layout" paths used across DRC runner, explorer, and demos.
    active_gds_state, set_active_gds = mo.state(
        "openEBL-2026-02/submissions/EBeam_solution_user.gds"
    )
    active_lyrdb_state, set_active_lyrdb = mo.state(
        "openEBL-2026-02/submissions/EBeam_solution_user.lyrdb"
    )

    # When set to 1, the explorer will auto-parse once, then reset to 0.
    drc_autoload_state, set_drc_autoload = mo.state(0)

    return (
        active_gds_state,
        active_lyrdb_state,
        drc_autoload_state,
        set_active_gds,
        set_active_lyrdb,
        set_drc_autoload,
    )


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
        title="Verifying the MZI layout",
        subtitle=(
            "Use the openEBL verification workflow to ensure your layout passes checks "
            "before you push to GitHub. Includes interactive tools for DFT validation, "
            "DRC checking, and common error diagnosis."
        ),
        badges=["Week 3", "Lab companion", "Verification", "openEBL workflow"],
        toc=[
            ("Overview", "overview"),
            ("Interactive Checklist", "checklist"),
            ("DFT Calculator", "dft-calculator"),
            ("DRC Runner", "drc-runner"),
            ("Layout Demo", "layout-demo"),
            ("Exercises", "exercises"),
            ("KLayout Guide", "klayout-guide"),
        ],
        build="2025-12-16",
    )
    return


@app.cell
def _(mo):
    from _notebook_template import make_health_refresh_button

    health_refresh = make_health_refresh_button(mo)
    return


@app.cell
def _(doc_callout_list, mo, show_overview):
    mo.stop(not show_overview)
    overview_md = mo.md(r"""
    <a id="overview"></a>
    ## Overview

    Week 2 helped you connect **ΔL ↔ FSR** and build basic intuition for an MZI spectrum.
    This week is about the **verification pipeline** that keeps your openEBL submission green.

    Week 2 references:
    - `marimo_course/lessons/w02_mzi_modelling.py` (rule-of-thumb, spectrum intuition)
    - `marimo_course/lessons/w02_pdk_mzi_layout.py` (PDK layout workflow + submission layers)
    """)

    definitions = doc_callout_list(
        "info",
        tag="Definitions",
        title="What we mean by verification",
        items=[
            "<strong>Verification</strong>: checking that the layout obeys PDK/openEBL rules so it passes automated checks "
            "(ports, labels, floorplan, DFT rules, and CI).",
            "<strong>DRC (Design Rule Check)</strong>: automated geometric checks for minimum widths, spaces, and layer relationships.",
            "<strong>DFT (Design for Test)</strong>: rules ensuring your circuit can be measured on the automated probe station.",
        ],
    )

    goals = doc_callout_list(
        "info",
        tag="Goals (lab)",
        title="What you should be able to do by the end",
        ordered=True,
        items=[
            "Run a verification checklist before pushing to GitHub/openEBL.",
            "Validate DFT requirements (pitch, orientation, opt_in placement) using the calculator.",
            "Run batch DRC and interpret the results.",
            "Understand why CI checks fail and how to debug them in KLayout.",
        ],
    )

    submission_note = doc_callout_list(
        "warning",
        tag="Where do I submit work?",
        title="Lab companion vs homework",
        items=[
            "This notebook is a lab companion (guided workflow + checklists).",
            "Graded work should live in the week-aligned homework notebook (e.g., `marimo_course/assignments/hw03_...`).",
        ],
    )
    mo.vstack([overview_md, definitions, goals, submission_note])
    return


@app.cell
def _():
    import numpy as np
    return (np,)


# ============================================================================
# SECTION: Interactive Pre-Push Checklist
# ============================================================================


@app.cell
def _(mo, show_checklist):
    mo.stop(not show_checklist)
    mo.md(r"""
    <a id="checklist"></a>
    ## Interactive Pre-Push Checklist

    Use this checklist before every push to the openEBL repository.
    Check off items as you complete them to track your progress.
    """)
    return


@app.cell
def _(mo, show_checklist):
    mo.stop(not show_checklist)

    # Create interactive checkboxes for the pre-push checklist
    check_pdk_loaded = mo.ui.checkbox(
        label="1. Opened design in KLayout with SiEPIC-EBeam PDK loaded",
        value=False,
    )
    check_ports = mo.ui.checkbox(
        label="2. Confirmed ports/pins/DevRec match PDK expectations",
        value=False,
    )
    check_gc_pitch = mo.ui.checkbox(
        label="3. Verified grating couplers are on 127 µm pitch",
        value=False,
    )
    check_gc_spacing = mo.ui.checkbox(
        label="4. Verified minimum GC spacing ≥ 60 µm",
        value=False,
    )
    check_gc_orientation = mo.ui.checkbox(
        label="5. Verified GC orientation is 0° (for ebeam_gc_te1550/tm1550)",
        value=False,
    )
    check_opt_in = mo.ui.checkbox(
        label="6. opt_in label within 10 µm of GC tip (if required)",
        value=False,
    )
    check_floorplan = mo.ui.checkbox(
        label="7. Layout is within floorplan boundaries",
        value=False,
    )
    check_drc = mo.ui.checkbox(
        label="8. Ran local DRC verification (no critical errors)",
        value=False,
    )
    check_top_cell = mo.ui.checkbox(
        label="9. Top-cell name follows naming convention",
        value=False,
    )
    check_export = mo.ui.checkbox(
        label="10. Exported GDS/OAS and re-opened to verify",
        value=False,
    )

    checklist_items = [
        check_pdk_loaded,
        check_ports,
        check_gc_pitch,
        check_gc_spacing,
        check_gc_orientation,
        check_opt_in,
        check_floorplan,
        check_drc,
        check_top_cell,
        check_export,
    ]
    mo.vstack(checklist_items)
    return (
        check_drc,
        check_export,
        check_floorplan,
        check_gc_orientation,
        check_gc_pitch,
        check_gc_spacing,
        check_opt_in,
        check_pdk_loaded,
        check_ports,
        check_top_cell,
        checklist_items,
    )


@app.cell
def _(checklist_items, mo, show_checklist):
    mo.stop(not show_checklist)

    # Calculate progress
    completed = sum(1 for item in checklist_items if item.value)
    total = len(checklist_items)
    progress_pct = (completed / total) * 100

    # Create progress indicator
    if completed == total:
        status_emoji = "✅"
        status_text = "Ready to push!"
        status_kind = "success"
    elif completed >= total * 0.7:
        status_emoji = "🔶"
        status_text = "Almost there..."
        status_kind = "warn"
    else:
        status_emoji = "⏳"
        status_text = "Keep going..."
        status_kind = "info"

    progress_bar = f"""
    <div style="background: #e0e0e0; border-radius: 8px; height: 24px; width: 100%; margin: 8px 0;">
        <div style="background: {'#4caf50' if completed == total else '#ff9800'};
                    border-radius: 8px; height: 24px; width: {progress_pct}%;
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-weight: bold; font-size: 12px;">
            {completed}/{total}
        </div>
    </div>
    """

    mo.callout(
        mo.md(f"""
**Checklist Progress** {status_emoji}

{progress_bar}

**Status:** {status_text} ({completed}/{total} items completed)
"""),
        kind=status_kind,
    )
    return completed, progress_pct, status_emoji, status_kind, status_text, total


# ============================================================================
# SECTION: DFT Validation Calculator
# ============================================================================


@app.cell
def _(mo, show_dft):
    mo.stop(not show_dft)
    mo.md(r"""
    <a id="dft-calculator"></a>
    ## DFT Validation Calculator

    Enter your grating coupler positions to validate against the DFT rules from the EBeam PDK.
    The calculator checks pitch, spacing, and array configuration requirements.

    **DFT Rules (from `SiEPIC_EBeam_PDK/klayout/EBeam/DFT.xml`):**
    - GC array pitch: **127 µm** (vertical)
    - Minimum GC spacing: **60 µm**
    - GC array orientation: **90°** (vertical array)
    - Max detectors above laser: **1**
    - Max detectors below laser: **2**
    - opt_in label: within **10 µm** of GC tip
    """)
    return


@app.cell
def _(mo, show_dft):
    mo.stop(not show_dft)

    # Input fields for GC positions
    gc1_y = mo.ui.number(value=0.0, label="GC 1 Y position (µm)", step=0.1)
    gc2_y = mo.ui.number(value=127.0, label="GC 2 Y position (µm)", step=0.1)
    gc3_y = mo.ui.number(value=254.0, label="GC 3 Y position (µm) [optional]", step=0.1)
    gc_orientation = mo.ui.number(value=0.0, label="GC cell orientation (°)", step=1.0)
    opt_in_distance = mo.ui.number(
        value=5.0, label="Distance from opt_in label to GC tip (µm)", step=0.1
    )
    laser_gc_index = mo.ui.dropdown(
        options=["GC 1 (input)", "GC 2", "GC 3"],
        value="GC 1 (input)",
        label="Which GC is the laser input?",
    )

    mo.vstack(
        [
            mo.md("### Enter Grating Coupler Positions"),
            mo.hstack([gc1_y, gc2_y, gc3_y]),
            mo.hstack([gc_orientation, opt_in_distance]),
            laser_gc_index,
        ]
    )
    return gc1_y, gc2_y, gc3_y, gc_orientation, laser_gc_index, opt_in_distance


@app.cell
def _(
    gc1_y,
    gc2_y,
    gc3_y,
    gc_orientation,
    laser_gc_index,
    mo,
    np,
    opt_in_distance,
    show_dft,
):
    mo.stop(not show_dft)

    # DFT rule constants
    REQUIRED_PITCH = 127.0  # µm
    MIN_SPACING = 60.0  # µm
    MAX_OPT_IN_DISTANCE = 10.0  # µm
    REQUIRED_GC_ORIENTATION = 0.0  # degrees for ebeam_gc_te1550
    MAX_DETECTORS_ABOVE = 1
    MAX_DETECTORS_BELOW = 2
    PITCH_TOLERANCE = 0.5  # µm tolerance for pitch matching

    # Collect GC positions
    positions = [gc1_y.value, gc2_y.value]
    if gc3_y.value != 0.0 or gc3_y.value != gc2_y.value:
        positions.append(gc3_y.value)
    positions = sorted(positions)

    # Calculate metrics
    results = []

    # 1. Check pitch (difference between adjacent GCs)
    pitches = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
    for i, pitch in enumerate(pitches):
        pitch_ok = abs(pitch - REQUIRED_PITCH) <= PITCH_TOLERANCE
        results.append(
            {
                "rule": f"Pitch GC{i+1}→GC{i+2}",
                "value": f"{pitch:.1f} µm",
                "required": f"{REQUIRED_PITCH} µm (±{PITCH_TOLERANCE})",
                "status": "✅ PASS" if pitch_ok else "❌ FAIL",
                "passed": pitch_ok,
            }
        )

    # 2. Check minimum spacing
    min_spacing = min(pitches) if pitches else 0
    spacing_ok = min_spacing >= MIN_SPACING
    results.append(
        {
            "rule": "Minimum GC spacing",
            "value": f"{min_spacing:.1f} µm",
            "required": f"≥ {MIN_SPACING} µm",
            "status": "✅ PASS" if spacing_ok else "❌ FAIL",
            "passed": spacing_ok,
        }
    )

    # 3. Check GC orientation
    orientation_ok = abs(gc_orientation.value - REQUIRED_GC_ORIENTATION) < 0.1
    results.append(
        {
            "rule": "GC orientation",
            "value": f"{gc_orientation.value}°",
            "required": f"{REQUIRED_GC_ORIENTATION}°",
            "status": "✅ PASS" if orientation_ok else "❌ FAIL",
            "passed": orientation_ok,
        }
    )

    # 4. Check opt_in distance
    opt_in_ok = opt_in_distance.value <= MAX_OPT_IN_DISTANCE
    results.append(
        {
            "rule": "opt_in label distance",
            "value": f"{opt_in_distance.value} µm",
            "required": f"≤ {MAX_OPT_IN_DISTANCE} µm",
            "status": "✅ PASS" if opt_in_ok else "❌ FAIL",
            "passed": opt_in_ok,
        }
    )

    # 5. Check detectors above/below laser
    laser_idx = {"GC 1 (input)": 0, "GC 2": 1, "GC 3": 2}.get(laser_gc_index.value, 0)
    laser_y = positions[laser_idx] if laser_idx < len(positions) else positions[0]
    detectors_above = sum(1 for p in positions if p > laser_y)
    detectors_below = sum(1 for p in positions if p < laser_y)

    above_ok = detectors_above <= MAX_DETECTORS_ABOVE
    below_ok = detectors_below <= MAX_DETECTORS_BELOW

    results.append(
        {
            "rule": "Detectors above laser",
            "value": str(detectors_above),
            "required": f"≤ {MAX_DETECTORS_ABOVE}",
            "status": "✅ PASS" if above_ok else "❌ FAIL",
            "passed": above_ok,
        }
    )
    results.append(
        {
            "rule": "Detectors below laser",
            "value": str(detectors_below),
            "required": f"≤ {MAX_DETECTORS_BELOW}",
            "status": "✅ PASS" if below_ok else "❌ FAIL",
            "passed": below_ok,
        }
    )

    # Build results table
    table_rows = "".join(
        f"<tr><td>{r['rule']}</td><td>{r['value']}</td><td>{r['required']}</td><td>{r['status']}</td></tr>"
        for r in results
    )
    table_html = f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Rule</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Your Value</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Required</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Status</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """

    all_passed = all(r["passed"] for r in results)
    summary_kind = "success" if all_passed else "warn"
    summary_text = (
        "All DFT checks passed! Your GC configuration meets the requirements."
        if all_passed
        else "Some DFT checks failed. Review the table above and adjust your layout."
    )

    mo.vstack(
        [
            mo.md("### DFT Validation Results"),
            mo.md(table_html),
            mo.callout(mo.md(f"**Summary:** {summary_text}"), kind=summary_kind),
        ]
    )
    return (
        MAX_DETECTORS_ABOVE,
        MAX_DETECTORS_BELOW,
        MAX_OPT_IN_DISTANCE,
        MIN_SPACING,
        PITCH_TOLERANCE,
        REQUIRED_GC_ORIENTATION,
        REQUIRED_PITCH,
        above_ok,
        all_passed,
        below_ok,
        detectors_above,
        detectors_below,
        laser_idx,
        laser_y,
        min_spacing,
        opt_in_ok,
        orientation_ok,
        pitches,
        positions,
        results,
        spacing_ok,
        summary_kind,
        summary_text,
        table_html,
        table_rows,
    )


# ============================================================================
# SECTION: Interactive DRC Runner
# ============================================================================


@app.cell
def _(mo, show_drc):
    mo.stop(not show_drc)
    mo.md(r"""
    <a id="drc-runner"></a>
    ## Interactive DRC Runner

    Run batch DRC (Design Rule Check) on your GDS file directly from this notebook.
    The tool uses KLayout's batch mode with the SiEPIC EBeam DRC deck.

    **Do this in order (recommended):**
    1. Run DRC on your active GDS (this section).
    2. Load the errors into the Visual DRC Error Explorer.
    3. Zoom/pan, understand the rule, fix in layout, and re-run.

    **Requirements:**
    - KLayout must be installed and accessible (in PATH or at `/Applications/KLayout.app`)
    - Your GDS file must exist at the specified path
    """)
    return


@app.cell
def _(active_gds_state, mo, set_active_gds, show_drc):
    mo.stop(not show_drc)

    # DRC input controls
    drc_gds_path = mo.ui.text(
        value=active_gds_state(),
        on_change=set_active_gds,
        label="GDS file path",
        full_width=True,
    )
    drc_run_button = mo.ui.button(
        value=0, label="Run DRC", kind="success", on_click=lambda v: (v or 0) + 1
    )

    mo.vstack([drc_gds_path, drc_run_button])
    return drc_gds_path, drc_run_button


@app.cell
def _(drc_gds_path, drc_run_button, mo, set_active_lyrdb, set_drc_autoload, show_drc):
    mo.stop(not show_drc)
    import subprocess
    from pathlib import Path
    import xml.etree.ElementTree as ET

    drc_output = []

    if drc_run_button.value > 0:
        gds_path = Path(drc_gds_path.value)

        if not gds_path.exists():
            drc_output.append(
                mo.callout(
                    mo.md(f"**Error:** GDS file not found at `{gds_path}`"),
                    kind="danger",
                )
            )
        else:
            # Define paths
            script_path = Path("marimo_course/scripts/run_klayout_drc.sh")
            output_lyrdb = gds_path.with_suffix(".lyrdb")

            if not script_path.exists():
                drc_output.append(
                    mo.callout(
                        mo.md(f"**Error:** DRC script not found at `{script_path}`"),
                        kind="danger",
                    )
                )
            else:
                try:
                    # Run the DRC script
                    result = subprocess.run(
                        ["bash", str(script_path), str(gds_path), str(output_lyrdb)],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )

                    if result.returncode != 0:
                        drc_output.append(
                            mo.callout(
                                mo.md(
                                    f"**DRC script error:**\n```\n{result.stderr}\n```"
                                ),
                                kind="danger",
                            )
                        )
                    else:
                        set_active_lyrdb(str(output_lyrdb))
                        set_drc_autoload(1)
                        drc_output.append(
                            mo.callout(
                                mo.md(
                                    f"**DRC completed.** Report: `{output_lyrdb}`\n\n"
                                    "Tip: the Visual DRC Error Explorer is now pointing at this report."
                                ),
                                kind="success",
                            )
                        )

                        # Parse the lyrdb file
                        if output_lyrdb.exists():
                            tree = ET.parse(output_lyrdb)
                            root = tree.getroot()

                            # Count errors by category
                            error_counts = {}
                            for item in root.findall(".//item"):
                                category = item.find("category")
                                if category is not None:
                                    cat_name = category.text.strip("'")
                                    error_counts[cat_name] = (
                                        error_counts.get(cat_name, 0) + 1
                                    )

                            if error_counts:
                                # Build error summary table
                                error_rows = "".join(
                                    f"<tr><td>{cat}</td><td style='text-align:center;'>{count}</td></tr>"
                                    for cat, count in sorted(error_counts.items())
                                )
                                error_table = f"""
                                <table style="width: 100%; border-collapse: collapse; margin-top: 8px;">
                                    <thead>
                                        <tr style="background: #ffebee;">
                                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Error Category</th>
                                            <th style="padding: 8px; border: 1px solid #ddd; text-align: center;">Count</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {error_rows}
                                    </tbody>
                                </table>
                                """
                                total_errors = sum(error_counts.values())
                                drc_output.append(
                                    mo.md(
                                        f"### DRC Errors Found: {total_errors}\n{error_table}"
                                    )
                                )
                            else:
                                drc_output.append(
                                    mo.callout(
                                        mo.md("**No DRC errors found!** Your layout passes all checks."),
                                        kind="success",
                                    )
                                )
                except subprocess.TimeoutExpired:
                    drc_output.append(
                        mo.callout(
                            mo.md("**Error:** DRC timed out after 120 seconds."),
                            kind="danger",
                        )
                    )
                except FileNotFoundError:
                    drc_output.append(
                        mo.callout(
                            mo.md(
                                "**Error:** KLayout not found. Make sure KLayout is installed and in your PATH."
                            ),
                            kind="danger",
                        )
                    )
                except Exception as e:
                    drc_output.append(
                        mo.callout(
                            mo.md(f"**Error:** {type(e).__name__}: {e}"), kind="danger"
                        )
                    )
    else:
        drc_output.append(
            mo.md("Click **Run DRC** to check your GDS file for design rule violations.")
        )

    mo.vstack(drc_output)
    return ET, Path, drc_output, gds_path, output_lyrdb, result, script_path, subprocess


@app.cell
def _(doc_callout_list, mo, show_drc):
    mo.stop(not show_drc)

    doc_callout_list(
        "info",
        tag="DRC Rules",
        title="What the DRC checks (from SiEPIC_EBeam_batch.drc)",
        items=[
            "<strong>Focus (this course layout)</strong>: silicon photonics layouts using Si + PinRec + DevRec + Floorplan (no SiN or metals).",
            "<strong>Si width/space</strong>: minimum feature size and spacing (Si layer 1/0).",
            "<strong>DevRec overlap</strong>: devices cannot overlap",
            "<strong>Boundary check</strong>: devices must be inside floorplan layer (99/0)",
            "<strong>PinRec check</strong>: pins must be inside Si/SiN to indicate a real waveguide connection",
            "<strong>Advanced (still in deck)</strong>: SiN and metal rules exist, but are not the focus for this assignment.",
        ],
    )
    return


# ============================================================================
# SECTION: Visual DRC Error Explorer
# ============================================================================


@app.cell
def _(mo, show_drc):
    mo.stop(not show_drc)
    mo.md(r"""
    ### Visual DRC Error Explorer

    Load a GDS file and its corresponding `.lyrdb` error report to visualize
    each DRC error with a zoomed view of the problem area.
    """)
    return


@app.cell
def _(mo, show_drc):
    mo.stop(not show_drc)
    mo.md(r"""
    #### Generate example DRC error cases

    This creates small, intentionally-broken GDS files and runs the local KLayout DRC to
    generate matching `.lyrdb` reports. Use these files to practice reading and visualizing
    common errors.
    """)

    examples_dir = mo.ui.text(
        value="openEBL-2026-02/drc_examples",
        label="Output folder for examples",
        full_width=True,
    )
    generate_examples = mo.ui.button(
        value=0,
        label="Generate example error GDS + LYRDB files",
        kind="warn",
        on_click=lambda v: (v or 0) + 1,
    )
    mo.vstack([examples_dir, generate_examples])
    return examples_dir, generate_examples


@app.cell
def _(examples_dir, generate_examples, mo, show_drc):
    mo.stop(not show_drc)
    mo.stop(generate_examples.value == 0)

    from _notebook_template import optional_import as _opt_import_examples

    _gf, _gf_err = _opt_import_examples("gdsfactory")
    if _gf is None:
        mo.output.replace(
            mo.callout(
                mo.md(f"**gdsfactory not available:** {_gf_err}"),
                kind="warn",
            )
        )
        mo.stop(True)

    import subprocess as _ex_subprocess
    import xml.etree.ElementTree as _ex_ET
    from pathlib import Path as _ExPath

    _ex_out_dir = _ExPath(examples_dir.value).expanduser()
    _ex_out_dir.mkdir(parents=True, exist_ok=True)

    _ex_script = _ExPath("marimo_course/scripts/run_klayout_drc.sh").resolve()
    if not _ex_script.exists():
        mo.output.replace(
            mo.callout(
                mo.md(f"**DRC script not found:** `{_ex_script}`"),
                kind="danger",
            )
        )
        mo.stop(True)

    def _rect(x0, y0, w, h):
        return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]

    def _add_floorplan(c, x0=-100, y0=-100, w=200, h=200):
        c.add_polygon(_rect(x0, y0, w, h), layer=(99, 0))

    def _write_case(case_key, builder):
        _gds_path = _ex_out_dir / f"example_{case_key}.gds"
        _lyrdb_path = _gds_path.with_suffix(".lyrdb")

        c = _gf.Component(name=f"drc_example_{case_key}")
        builder(c)
        c.write_gds(_gds_path)

        result = _ex_subprocess.run(
            ["bash", str(_ex_script), str(_gds_path), str(_lyrdb_path)],
            capture_output=True,
            text=True,
            timeout=240,
        )

        error_count = None
        if _lyrdb_path.exists():
            try:
                root = _ex_ET.parse(_lyrdb_path).getroot()
                error_count = len(root.findall(".//item"))
            except Exception:
                error_count = None

        return _gds_path, _lyrdb_path, result.returncode, error_count, result.stderr.strip()

    cases = []

    # Boundary: put Si outside floorplan box.
    cases.append(
        (
            "Boundary",
            lambda c: (
                c.add_polygon(_rect(-20, -20, 40, 40), layer=(99, 0)),
                c.add_polygon(_rect(30, 0, 20, 2), layer=(1, 0)),
            ),
        )
    )

    # Si feature/space
    cases.append(
        (
            "Si_width",
            lambda c: (
                _add_floorplan(c),
                c.add_polygon(_rect(-10, -10, 20, 0.05), layer=(1, 0)),
            ),
        )
    )
    cases.append(
        (
            "Si_space",
            lambda c: (
                _add_floorplan(c),
                c.add_polygon(_rect(-10, -10, 20, 0.5), layer=(1, 0)),
                c.add_polygon(_rect(-10, -10 + 0.5 + 0.03, 20, 0.5), layer=(1, 0)),
            ),
        )
    )


    # PinRec not inside Si/SiN (SiEPIC-1a)
    cases.append(
        (
            "SiEPIC_1a",
            lambda c: (
                _add_floorplan(c),
                c.add_polygon(_rect(-5, -5, 2.0, 1.0), layer=(1, 10)),
            ),
        )
    )

    # Devices overlap: two DevRec boxes overlapping.
    cases.append(
        (
            "Devices",
            lambda c: (
                _add_floorplan(c),
                c.add_polygon(_rect(-20, -10, 30.0, 20.0), layer=(68, 0)),
                c.add_polygon(_rect(-5, -10, 30.0, 20.0), layer=(68, 0)),
            ),
        )
    )

    _ex_rows = []
    for case_key, builder in cases:
        try:
            _gds_path, _lyrdb_path, _rc, _n_items, _stderr = _write_case(case_key, builder)
            _status = "OK" if _rc == 0 else f"DRC exit {_rc}"
            _details = f"{_n_items} items" if isinstance(_n_items, int) else "items unknown"
            _ex_rows.append(
                (case_key, str(_gds_path), str(_lyrdb_path), _status, _details, _stderr)
            )
        except _ex_subprocess.TimeoutExpired:
            _ex_rows.append((case_key, "?", "?", "DRC timeout", "", ""))
        except Exception as e:
            _ex_rows.append((case_key, "?", "?", f"{type(e).__name__}", "", str(e)))

    _examples_table_rows = "\n".join(
        f"<tr><td><code>{k}</code></td><td><code>{g}</code></td><td><code>{l}</code></td><td>{s}</td><td>{d}</td></tr>"
        for (k, g, l, s, d, _stderr) in _ex_rows
    )
    _examples_table_html = f"""
    <table style="width: 100%; border-collapse: collapse; margin-top: 8px;">
        <thead>
            <tr>
                <th style="padding: 6px; border: 1px solid #ddd; text-align: left;">Case</th>
                <th style="padding: 6px; border: 1px solid #ddd; text-align: left;">GDS</th>
                <th style="padding: 6px; border: 1px solid #ddd; text-align: left;">LYRDB</th>
                <th style="padding: 6px; border: 1px solid #ddd; text-align: left;">DRC</th>
                <th style="padding: 6px; border: 1px solid #ddd; text-align: left;">Report</th>
            </tr>
        </thead>
        <tbody>
            {_examples_table_rows}
        </tbody>
    </table>
    """

    mo.output.replace(
        mo.vstack(
            [
                mo.callout(
                    mo.md(f"Generated {len(_ex_rows)} example cases in `{_ex_out_dir}`."),
                    kind="success",
                ),
                mo.Html(_examples_table_html),
            ]
        )
    )
    return


@app.cell
def _(examples_dir, mo, set_active_gds, set_active_lyrdb, set_drc_autoload, show_drc):
    mo.stop(not show_drc)

    from _drc_helpers import list_example_pairs as _list_example_pairs
    from pathlib import Path as _SelPath

    examples_root = _SelPath(examples_dir.value).expanduser()
    example_pairs = _list_example_pairs(examples_root)

    example_options = {
        _gds.stem.replace("example_", ""): str(_gds)
        for _gds, _lyrdb in example_pairs
    }

    selected_example_state, set_selected_example = mo.state(None)

    def _on_select_example(value: str | None):
        set_selected_example(value)
        if not value:
            return
        _gds = _SelPath(value)
        _lyrdb = _gds.with_suffix(".lyrdb")
        if _gds.exists() and _lyrdb.exists():
            set_active_gds(str(_gds))
            set_active_lyrdb(str(_lyrdb))
            set_drc_autoload(1)

    example_picker = mo.ui.dropdown(
        options=example_options,
        value=selected_example_state(),
        label="Select an example (auto-fills the paths below)",
        on_change=_on_select_example,
        full_width=True,
    )

    picker_status = (
        mo.callout(
            mo.md(
                f"No examples found in `{examples_root}` yet. Click **Generate example error GDS + LYRDB files** first."
            ),
            kind="info",
        )
        if not example_options
        else mo.md("")
    )

    return (
        example_pairs,
        example_options,
        example_picker,
        examples_root,
        picker_status,
        selected_example_state,
    )


@app.cell
def _(
    active_gds_state,
    active_lyrdb_state,
    example_picker,
    picker_status,
    mo,
    set_active_gds,
    set_active_lyrdb,
    show_drc,
):
    mo.stop(not show_drc)

    explorer_gds_path = mo.ui.text(
        value=active_gds_state(),
        on_change=set_active_gds,
        label="GDS file path",
        full_width=True,
    )
    explorer_lyrdb_path = mo.ui.text(
        value=active_lyrdb_state(),
        on_change=set_active_lyrdb,
        label="LYRDB error report path",
        full_width=True,
    )
    load_errors_button = mo.ui.button(
        value=0,
        label="Load Errors",
        kind="success",
        on_click=lambda v: (v or 0) + 1,
    )

    explorer_ui = mo.vstack(
        [
            example_picker,
            picker_status,
            explorer_gds_path,
            explorer_lyrdb_path,
            load_errors_button,
        ]
    )
    explorer_ui
    return explorer_gds_path, explorer_lyrdb_path, load_errors_button, explorer_ui


@app.cell
def _(
    drc_autoload_state,
    explorer_gds_path,
    explorer_lyrdb_path,
    load_errors_button,
    mo,
    set_drc_autoload,
    show_drc,
):
    mo.stop(not show_drc)
    from pathlib import Path as _ExpPath
    from _drc_helpers import parse_lyrdb_errors as parse_lyrdb_errors

    # State for parsed errors
    parsed_errors = []
    _error_load_status = None

    _autoload = drc_autoload_state()
    if load_errors_button.value > 0 or _autoload > 0:
        _explorer_gds = _ExpPath(explorer_gds_path.value)
        _explorer_lyrdb = _ExpPath(explorer_lyrdb_path.value)

        if not _explorer_gds.exists():
            _error_load_status = mo.callout(
                mo.md(f"**Error:** GDS file not found at `{_explorer_gds}`"),
                kind="danger",
            )
        elif not _explorer_lyrdb.exists():
            _error_load_status = mo.callout(
                mo.md(f"**Error:** LYRDB file not found at `{_explorer_lyrdb}`"),
                kind="danger",
            )
        else:
            try:
                parsed_errors = parse_lyrdb_errors(_explorer_lyrdb)
                if parsed_errors:
                    _error_load_status = mo.callout(
                        mo.md(f"**Loaded {len(parsed_errors)} errors** from `{_explorer_lyrdb.name}`"),
                        kind="success",
                    )
                else:
                    _error_load_status = mo.callout(
                        mo.md("**No errors found** in the LYRDB file."),
                        kind="success",
                    )
            except Exception as e:
                _error_load_status = mo.callout(
                    mo.md(f"**Error parsing LYRDB:** {type(e).__name__}: {e}"),
                    kind="danger",
                )

        if _autoload > 0:
            set_drc_autoload(0)

    if _error_load_status:
        mo.output.replace(_error_load_status)
    else:
        mo.output.replace(mo.md("Click **Load Errors** to parse the LYRDB file."))

    parsed_errors
    return parse_lyrdb_errors, parsed_errors


@app.cell
def _(explorer_gds_path, mo, parsed_errors, show_drc):
    mo.stop(not show_drc)
    mo.stop(len(parsed_errors) == 0)

    # Create dropdown options for each error
    error_options = {
        f"{i+1}. {e['category']} @ ({e['center_x']:.1f}, {e['center_y']:.1f})": i
        for i, e in enumerate(parsed_errors)
    }

    error_selector = mo.ui.dropdown(
        options=error_options,
        value=list(error_options.keys())[0] if error_options else None,
        label="Select error to visualize",
        full_width=True,
    )

    zoom_radius = mo.ui.slider(
        start=1,
        stop=50,
        value=10,
        step=1,
        label="Zoom radius (µm)",
        show_value=True,
    )

    show_debug = mo.ui.checkbox(
        label="Show debug details (bbox, coordinate mismatch)",
        value=False,
    )

    mo.vstack([error_selector, zoom_radius, show_debug])
    return error_options, error_selector, show_debug, zoom_radius


@app.cell
def _(error_selector, explorer_gds_path, mo, parsed_errors, show_debug, show_drc, zoom_radius):
    mo.stop(not show_drc)
    mo.stop(len(parsed_errors) == 0)
    mo.stop(error_selector.value is None)

    from _notebook_template import optional_import as _opt_import_explorer

    _gf_explorer, _gf_explorer_err = _opt_import_explorer("gdsfactory")

    _explorer_output = []

    if _gf_explorer is None:
        _explorer_output.append(
            mo.callout(
                mo.md(f"**gdsfactory not available:** {_gf_explorer_err}"),
                kind="warn",
            )
        )
    else:
        try:
            from pathlib import Path as _GfPath
            from gdsfactory.read import import_gds as _import_gds_explorer
            import matplotlib.pyplot as _plt_explorer
            import matplotlib.patches as _mpatches
            from matplotlib.collections import PatchCollection
            from io import BytesIO as _ExplorerBytesIO

            _alt, _alt_err = _opt_import_explorer("altair")
            _pd, _pd_err = _opt_import_explorer("pandas")

            # Get selected error
            _error_idx = error_selector.value
            _error = parsed_errors[_error_idx]

            # Load the GDS
            _exp_gds_path = _GfPath(explorer_gds_path.value)
            _exp_component = _import_gds_explorer(_exp_gds_path)

            # Create zoomed plot centered on error location
            _center_x = _error["center_x"]
            _center_y = _error["center_y"]
            _radius = zoom_radius.value

            # Get the component bounding box for reference (handle different gdsfactory versions)
            _bbox = _exp_component.bbox
            if callable(_bbox):
                _bbox = _bbox()
            # Handle different bbox formats (tuple vs DBox object)
            if hasattr(_bbox, '__getitem__'):
                _bbox_xmin, _bbox_ymin = _bbox[0]
                _bbox_xmax, _bbox_ymax = _bbox[1]
            elif hasattr(_bbox, 'left'):
                _bbox_xmin, _bbox_ymin = _bbox.left, _bbox.bottom
                _bbox_xmax, _bbox_ymax = _bbox.right, _bbox.top
            else:
                # Fallback: try p1/p2 attributes
                _bbox_xmin, _bbox_ymin = _bbox.p1.x, _bbox.p1.y
                _bbox_xmax, _bbox_ymax = _bbox.p2.x, _bbox.p2.y

            # Check if error location is within the GDS bounding box
            _error_in_bbox = (
                _bbox_xmin <= _center_x <= _bbox_xmax and
                _bbox_ymin <= _center_y <= _bbox_ymax
            )

            # Add debug info about coordinate mismatch
            _debug_info = f"""
**Debug Info:**
- GDS bounding box: X=[{_bbox_xmin:.1f}, {_bbox_xmax:.1f}], Y=[{_bbox_ymin:.1f}, {_bbox_ymax:.1f}]
- Error location: ({_center_x:.3f}, {_center_y:.3f})
- Error in GDS bounds: **{'Yes' if _error_in_bbox else 'NO - coordinate mismatch!'}**
"""
            if show_debug.value:
                _explorer_output.append(mo.md(_debug_info))

            # Create a fresh figure and axes for manual rendering
            _fig, _ax = _plt_explorer.subplots(figsize=(10, 8))

            # Set initial view window (used for plotting/filtering)
            if not _error_in_bbox:
                _view_xmin, _view_xmax = _bbox_xmin - 10, _bbox_xmax + 10
                _view_ymin, _view_ymax = _bbox_ymin - 10, _bbox_ymax + 10
            else:
                _view_xmin, _view_xmax = _center_x - _radius, _center_x + _radius
                _view_ymin, _view_ymax = _center_y - _radius, _center_y + _radius

            # Define layer colors (matching KLayout/gdsfactory conventions)
            _layer_colors = {
                (1, 0): ("#1f77b4", 0.7),   # Si - blue
                (1, 10): ("#ff7f0e", 0.5),  # PinRec - orange
                (4, 0): ("#2ca02c", 0.7),   # SiN - green
                (10, 0): ("#d62728", 0.3),  # Text - red
                (11, 0): ("#9467bd", 0.6),  # M1 - purple
                (12, 0): ("#8c564b", 0.6),  # M2 - brown
                (68, 0): ("#e377c2", 0.2),  # DevRec - pink
                (99, 0): ("#7f7f7f", 0.1),  # Floorplan - gray
            }

            _poly_rows = []
            _poly_id_counter = 0

            # Get all polygons from the component and draw them manually
            _total_polys = 0
            try:
                _dbu = getattr(getattr(_exp_component, "kcl", None), "dbu", 1.0)

                def _poly_points_um(_poly_obj):
                    # gdsfactory>=9 returns KLayout polygons; older versions may return numpy arrays.
                    if hasattr(_poly_obj, "each_point_hull"):
                        return [(p.x * _dbu, p.y * _dbu) for p in _poly_obj.each_point_hull()]
                    return _poly_obj

                _polygons_by_layer = _exp_component.get_polygons(by="tuple")
                if not _polygons_by_layer:
                    # Imported GDS is often hierarchical; flatten to materialize polygons.
                    _flat_component = _exp_component
                    try:
                        _flat_result = _flat_component.flatten()
                        if _flat_result is not None:
                            _flat_component = _flat_result
                    except Exception as _flat_err:
                        _explorer_output.append(
                            mo.callout(
                                mo.md(f"Note: Could not flatten component for plotting: {_flat_err}"),
                                kind="info",
                            )
                        )
                    _polygons_by_layer = _flat_component.get_polygons(by="tuple")
                for _layer_spec, _polys in _polygons_by_layer.items():
                    _color, _alpha = _layer_colors.get(_layer_spec, ("#bcbd22", 0.5))
                    for _poly in _polys:
                        _points = _poly_points_um(_poly)
                        if hasattr(_points, "tolist"):
                            _points = _points.tolist()
                        if not _points:
                            continue

                        _xs = [p[0] for p in _points]
                        _ys = [p[1] for p in _points]
                        if max(_xs) < _view_xmin or min(_xs) > _view_xmax or max(_ys) < _view_ymin or min(_ys) > _view_ymax:
                            continue

                        _total_polys += 1
                        _poly_id_counter += 1

                        if _points[0] != _points[-1]:
                            _points = list(_points) + [tuple(_points[0])]

                        _layer_label = f"{_layer_spec[0]}/{_layer_spec[1]}"
                        _patch = _mpatches.Polygon(
                            _points,
                            closed=True,
                            facecolor=_color,
                            edgecolor=_color,
                            alpha=_alpha,
                            linewidth=0.5,
                        )
                        _ax.add_patch(_patch)
                        for _j, (_x, _y) in enumerate(_points):
                            _poly_rows.append(
                                {
                                    "x": float(_x),
                                    "y": float(_y),
                                    "poly_id": str(_poly_id_counter),
                                    "layer": _layer_label,
                                    "j": _j,
                                }
                            )
                if _total_polys == 0:
                    # Fallback: use gdstk to extract polygons across hierarchy.
                    try:
                        import gdstk as _gdstk

                        _lib = _gdstk.read_gds(str(_exp_gds_path))
                        _top_cells = _lib.top_level()
                        if not _top_cells:
                            raise RuntimeError("No top-level cells found in GDS.")

                        _top = _top_cells[0]
                        _gdstk_polys = _top.get_polygons(include_paths=True, depth=None)
                        _gdstk_by_spec = {}
                        for _poly in _gdstk_polys:
                            _spec = (int(_poly.layer), int(_poly.datatype))
                            _gdstk_by_spec.setdefault(_spec, []).append(_poly.points)

                        for _layer_spec, _polys in _gdstk_by_spec.items():
                            _color, _alpha = _layer_colors.get(_layer_spec, ("#bcbd22", 0.5))
                            for _poly in _polys:
                                if hasattr(_poly, "tolist"):
                                    _poly = _poly.tolist()
                                if not _poly:
                                    continue

                                _xs = [p[0] for p in _poly]
                                _ys = [p[1] for p in _poly]
                                if max(_xs) < _view_xmin or min(_xs) > _view_xmax or max(_ys) < _view_ymin or min(_ys) > _view_ymax:
                                    continue

                                _total_polys += 1
                                _poly_id_counter += 1

                                if _poly[0] != _poly[-1]:
                                    _poly = list(_poly) + [tuple(_poly[0])]

                                _layer_label = f"{_layer_spec[0]}/{_layer_spec[1]}"
                                _patch = _mpatches.Polygon(
                                    _poly,
                                    closed=True,
                                    facecolor=_color,
                                    edgecolor=_color,
                                    alpha=_alpha,
                                    linewidth=0.5,
                                )
                                _ax.add_patch(_patch)
                                for _j, (_x, _y) in enumerate(_poly):
                                    _poly_rows.append(
                                        {
                                            "x": float(_x),
                                            "y": float(_y),
                                            "poly_id": str(_poly_id_counter),
                                            "layer": _layer_label,
                                            "j": _j,
                                        }
                                    )

                        if _total_polys == 0:
                            _explorer_output.append(
                                mo.callout(
                                    mo.md(
                                        "No polygons found to plot (gdsfactory and gdstk both returned empty). "
                                        "Double-check that the selected top cell contains geometry."
                                    ),
                                    kind="warn",
                                )
                            )
                    except Exception as _gdstk_err:
                        _explorer_output.append(
                            mo.callout(
                                mo.md(
                                    "No polygons found to plot via gdsfactory, and gdstk fallback failed: "
                                    f"{type(_gdstk_err).__name__}: {_gdstk_err}"
                                ),
                                kind="warn",
                            )
                        )
            except Exception as _poly_err:
                # Fallback: try to get polygons without by_spec
                _explorer_output.append(
                    mo.callout(
                        mo.md(f"Note: Could not get layer-specific polygons: {_poly_err}"),
                        kind="info",
                    )
                )

            # Force matplotlib to recognize the patches and compute data limits
            _ax.autoscale_view()

            # If error is outside bbox, show full layout with marker instead of zooming
            if not _error_in_bbox:
                # Show full layout - the error coords don't match the GDS coords
                _ax.set_xlim(_view_xmin, _view_xmax)
                _ax.set_ylim(_view_ymin, _view_ymax)
                if show_debug.value:
                    _explorer_output.insert(
                        0,
                        mo.callout(
                            mo.md(
                                f"**Coordinate mismatch detected!** The DRC error coordinates from the .lyrdb file "
                                f"({_center_x:.1f}, {_center_y:.1f}) are outside the GDS layout bounds. "
                                "This is common when the DRC was run on a different version of the file or with a different cell origin. "
                                "Showing full layout instead."
                            ),
                            kind="warn",
                        ),
                    )
                else:
                    _explorer_output.insert(
                        0,
                        mo.callout(
                            mo.md(
                                "**Coordinate mismatch detected.** Showing full layout (enable debug details for bbox info)."
                            ),
                            kind="warn",
                        ),
                    )
            else:
                # Set the view to be zoomed in on the error location
                _ax.set_xlim(_view_xmin, _view_xmax)
                _ax.set_ylim(_view_ymin, _view_ymax)

            # Add a marker at the error center
            _ax.plot(_center_x, _center_y, 'rx', markersize=20, markeredgewidth=4, label='Error location', zorder=100)

            # Draw a box around the error region if we have multiple coordinates
            if len(_error["all_x"]) >= 2:
                _x_min, _x_max = min(_error["all_x"]), max(_error["all_x"])
                _y_min, _y_max = min(_error["all_y"]), max(_error["all_y"])
                # Add some padding
                _pad = 0.2
                _rect = _mpatches.Rectangle(
                    (_x_min - _pad, _y_min - _pad),
                    (_x_max - _x_min) + 2 * _pad,
                    (_y_max - _y_min) + 2 * _pad,
                    linewidth=3,
                    edgecolor='red',
                    facecolor='none',
                    linestyle='--',
                    label='Error region',
                    zorder=99
                )
                _ax.add_patch(_rect)

            _ax.set_title(f"DRC Error: {_error['category']}", fontsize=14, fontweight='bold')
            _ax.set_xlabel("X (µm)")
            _ax.set_ylabel("Y (µm)")
            _ax.set_aspect('equal')
            _ax.legend(loc='upper right', fontsize=8)
            _ax.grid(True, alpha=0.3)

            # Save to buffer
            _buf = _ExplorerBytesIO()
            _fig.savefig(_buf, format="png", bbox_inches="tight", dpi=150)
            _buf.seek(0)
            _plt_explorer.close(_fig)

            _plot_outputs = {}
            if _alt is not None and _pd is not None and _poly_rows:
                try:
                    import altair as _altair
                    import pandas as _pandas

                    _df_polys = _pandas.DataFrame(_poly_rows)
                    _df_marker = _pandas.DataFrame([{"x": _center_x, "y": _center_y}])

                    _charts = []

                    _charts.append(
                        _altair.Chart(_df_polys)
                        .mark_line(strokeWidth=1)
                        .encode(
                            x=_altair.X("x:Q", title="X (µm)", scale=_altair.Scale(zero=False)),
                            y=_altair.Y("y:Q", title="Y (µm)", scale=_altair.Scale(zero=False)),
                            detail="poly_id:N",
                            color=_altair.Color("layer:N", legend=None),
                            order="j:Q",
                        )
                    )

                    if len(_error["all_x"]) >= 2:
                        _x_min, _x_max = min(_error["all_x"]), max(_error["all_x"])
                        _y_min, _y_max = min(_error["all_y"]), max(_error["all_y"])
                        _pad = 0.2
                        _df_rect = _pandas.DataFrame(
                            [
                                {
                                    "x0": _x_min - _pad,
                                    "x1": _x_max + _pad,
                                    "y0": _y_min - _pad,
                                    "y1": _y_max + _pad,
                                }
                            ]
                        )
                        _charts.append(
                            _altair.Chart(_df_rect)
                            .mark_rect(
                                fillOpacity=0.0,
                                stroke="red",
                                strokeDash=[6, 4],
                                strokeWidth=2,
                            )
                            .encode(
                                x=_altair.X("x0:Q", title="X (µm)"),
                                x2="x1:Q",
                                y=_altair.Y("y0:Q", title="Y (µm)"),
                                y2="y1:Q",
                            )
                        )

                    _charts.append(
                        _altair.Chart(_df_marker)
                        .mark_point(shape="cross", size=200, color="red")
                        .encode(x="x:Q", y="y:Q")
                    )

                    _interactive_chart = (
                        _altair.layer(*_charts)
                        .properties(
                            width=750,
                            height=550,
                            title=f"DRC Error: {_error['category']} (zoom/pan with mouse)",
                        )
                        .interactive()
                    )
                    _plot_outputs["Interactive (zoom/pan)"] = _interactive_chart
                except Exception as _altair_err:
                    _explorer_output.append(
                        mo.callout(
                            mo.md(
                                f"Could not render interactive plot: {type(_altair_err).__name__}: {_altair_err}"
                            ),
                            kind="warn",
                        )
                    )
            elif _alt is None or _pd is None:
                _missing = []
                if _alt is None:
                    _missing.append(f"altair: {_alt_err}")
                if _pd is None:
                    _missing.append(f"pandas: {_pd_err}")
                _explorer_output.append(
                    mo.callout(
                        mo.md("Interactive plot unavailable (" + ", ".join(_missing) + ")."),
                        kind="info",
                    )
                )

            _plot_outputs["Static (PNG)"] = mo.image(_buf)
            _explorer_output.append(mo.ui.tabs(_plot_outputs, value=list(_plot_outputs.keys())[0], lazy=True))

            # Error details
            _error_details = f"""
**Error Category:** `{_error['category']}`

**Description:** {_error['description']}

**Location:** ({_center_x:.3f}, {_center_y:.3f}) µm

**Raw DRC Output:**
```
{_error['raw_value']}
```
"""

            _explorer_output.append(mo.md(_error_details))

            # Add explanation based on error type
            _explanations = {
                "Si_space": """
**What this error means:** Two silicon features are closer than 70 nm apart.
This often occurs at waveguide bends, directional coupler gaps, or where routing
gets too close together.

**How to fix:** Increase the gap between the features to at least 70 nm.
""",
                "Si_width": """
**What this error means:** A silicon feature is narrower than 70 nm.
This can happen at tapered waveguide tips or narrow routing sections.

**How to fix:** Widen the feature to at least 70 nm, or adjust taper parameters.
""",
                "SiEPIC-1a": """
**What this error means:** A PinRec marker doesn't properly enclose exactly one
waveguide material (Si or SiN). This usually indicates a disconnected waveguide
or misaligned port marker.

**How to fix:** Ensure PinRec rectangles are centered on waveguide ports and
overlap the waveguide material. Check for unintended gaps at connections.
""",
                "Devices": """
**What this error means:** Two DevRec (device recognition) layers overlap.
Each component should have its own non-overlapping DevRec boundary.

**How to fix:** Move components apart so their DevRec boxes don't touch.
""",
                "Boundary": """
**What this error means:** Part of the layout extends outside the Floorplan
layer (99/0) boundary.

**How to fix:** Either move the design inside the floorplan or expand the
floorplan boundary to encompass all features.
""",
            }

            _explanation = _explanations.get(_error["category"], "")
            if _explanation:
                _explorer_output.append(
                    mo.callout(mo.md(_explanation.strip()), kind="info")
                )

        except Exception as e:
            import traceback
            _explorer_output.append(
                mo.callout(
                    mo.md(f"**Error rendering:** {type(e).__name__}: {e}\n\n```\n{traceback.format_exc()}\n```"),
                    kind="danger",
                )
            )

    mo.vstack(_explorer_output)
    return


@app.cell
def _(mo, parsed_errors, show_drc):
    mo.stop(not show_drc)
    mo.stop(len(parsed_errors) == 0)

    # Create summary of all errors by category
    _category_summary = {}
    for _err in parsed_errors:
        _cat = _err["category"]
        _category_summary[_cat] = _category_summary.get(_cat, 0) + 1

    _summary_rows = "".join(
        f"<tr><td>{cat}</td><td style='text-align:center'>{count}</td><td>{parsed_errors[[e['category'] for e in parsed_errors].index(cat)]['description']}</td></tr>"
        for cat, count in sorted(_category_summary.items())
    )

    _summary_table = f"""
### Error Summary by Category

<table style="width: 100%; border-collapse: collapse; margin: 8px 0;">
    <thead>
        <tr style="background: #fff3e0;">
            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Category</th>
            <th style="padding: 8px; border: 1px solid #ddd; text-align: center;">Count</th>
            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Description</th>
        </tr>
    </thead>
    <tbody>
        {_summary_rows}
    </tbody>
</table>

Use the dropdown above to select and visualize each individual error.
"""

    mo.md(_summary_table)
    return


# ============================================================================
# SECTION: Live Layout Inspection Demo
# ============================================================================


@app.cell
def _(mo, show_layout):
    mo.stop(not show_layout)
    mo.md(r"""
    <a id="layout-demo"></a>
    ## Live Layout Inspection Demo

    Load and visualize an example GDS file to understand the layer structure
    and verification-relevant elements (PinRec, DevRec, Floorplan).
    """)
    return


@app.cell
def _(active_gds_state, mo, set_active_gds, show_layout):
    mo.stop(not show_layout)

    demo_gds_path = mo.ui.text(
        value=active_gds_state(),
        on_change=set_active_gds,
        label="GDS file to inspect",
        full_width=True,
    )
    show_layers = mo.ui.checkbox(label="Show layer breakdown", value=True)
    load_demo_button = mo.ui.button(
        value=0, label="Load & Visualize", kind="success", on_click=lambda v: (v or 0) + 1
    )

    mo.vstack([demo_gds_path, mo.hstack([show_layers, load_demo_button])])
    return demo_gds_path, load_demo_button, show_layers


@app.cell
def _(demo_gds_path, load_demo_button, mo, show_layers, show_layout):
    mo.stop(not show_layout)

    from _notebook_template import optional_import

    gf_demo, gf_demo_error = optional_import("gdsfactory")

    demo_output = []

    if gf_demo is None:
        demo_output.append(
            mo.callout(
                mo.md(
                    f"**gdsfactory not available:** {gf_demo_error}\n\nInstall with `pip install gdsfactory`"
                ),
                kind="warn",
            )
        )
    elif load_demo_button.value > 0:
        from pathlib import Path as DemoPath

        demo_path = DemoPath(demo_gds_path.value)

        if not demo_path.exists():
            demo_output.append(
                mo.callout(
                    mo.md(f"**Error:** GDS file not found at `{demo_path}`"),
                    kind="danger",
                )
            )
        else:
            try:
                from gdsfactory.read import import_gds

                # Load the GDS
                component = import_gds(demo_path)

                # Get layer info
                if show_layers.value:
                    # Define known layers
                    layer_info = {
                        (1, 0): ("Si", "Silicon waveguide layer"),
                        (1, 10): ("PinRec", "Port/pin markers"),
                        (4, 0): ("SiN", "Silicon nitride layer"),
                        (10, 0): ("Text", "Text labels"),
                        (11, 0): ("M1", "Metal heater layer"),
                        (12, 0): ("M2", "Metal routing layer"),
                        (68, 0): ("DevRec", "Device recognition layer"),
                        (99, 0): ("Floorplan", "Chip boundary layer"),
                    }

                    # Get layers present in the GDS
                    if hasattr(component, "layers"):
                        present_layers = list(component.layers)
                    else:
                        present_layers = []

                    layer_rows = ""
                    for layer in sorted(present_layers):
                        name, desc = layer_info.get(layer, ("Unknown", "Custom layer"))
                        layer_rows += f"<tr><td>{layer}</td><td>{name}</td><td>{desc}</td></tr>"

                    if layer_rows:
                        layer_table = f"""
                        <table style="width: 100%; border-collapse: collapse; margin: 8px 0;">
                            <thead>
                                <tr style="background: #e3f2fd;">
                                    <th style="padding: 8px; border: 1px solid #ddd;">Layer</th>
                                    <th style="padding: 8px; border: 1px solid #ddd;">Name</th>
                                    <th style="padding: 8px; border: 1px solid #ddd;">Description</th>
                                </tr>
                            </thead>
                            <tbody>{layer_rows}</tbody>
                        </table>
                        """
                        demo_output.append(mo.md(f"### Layers in GDS\n{layer_table}"))

                # Plot the component
                fig = component.plot()
                if fig is None:
                    import matplotlib.pyplot as plt

                    fig = plt.gcf()

                from io import BytesIO

                buf = BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
                buf.seek(0)
                demo_output.append(mo.md("### Layout Preview"))
                demo_output.append(mo.image(buf))

                # Show bounding box info
                bbox = component.bbox
                if hasattr(bbox, "__getitem__"):
                    (xmin, ymin), (xmax, ymax) = bbox[0], bbox[1]
                    width = xmax - xmin
                    height = ymax - ymin
                    demo_output.append(
                        mo.md(
                            f"**Bounding box:** ({xmin:.1f}, {ymin:.1f}) to ({xmax:.1f}, {ymax:.1f}) "
                            f"— Size: {width:.1f} × {height:.1f} µm"
                        )
                    )

            except Exception as e:
                demo_output.append(
                    mo.callout(
                        mo.md(f"**Error loading GDS:** {type(e).__name__}: {e}"),
                        kind="danger",
                    )
                )
    else:
        demo_output.append(mo.md("Click **Load & Visualize** to inspect a GDS file."))

    mo.vstack(demo_output)
    return (
        BytesIO,
        DemoPath,
        bbox,
        buf,
        component,
        demo_output,
        demo_path,
        fig,
        gf_demo,
        gf_demo_error,
        height,
        import_gds,
        layer_info,
        layer_rows,
        layer_table,
        optional_import,
        plt,
        present_layers,
        width,
        xmax,
        xmin,
        ymax,
        ymin,
    )


# ============================================================================
# SECTION: Spot the Error & CI Debugger Exercises
# ============================================================================


@app.cell
def _(mo, show_exercises):
    mo.stop(not show_exercises)
    mo.md(r"""
    <a id="exercises"></a>
    ## Exercises: Spot the Error & CI Failure Debugger

    Practice identifying common verification errors and learn how to debug CI failures.
    """)
    return


@app.cell
def _(doc_callout_html, mo, show_exercises):
    mo.stop(not show_exercises)

    # Spot the Error scenarios
    mo.md("### Spot the Error")

    error_scenarios = [
        {
            "title": "Scenario 1: Missing PinRec",
            "description": "A student's MZI layout looks correct but fails CI with 'waveguide disconnect' errors.",
            "image_desc": "Layout shows waveguides connecting to grating couplers, but no PinRec rectangles on the ports.",
            "error": "Missing PinRec markers on external ports",
            "fix": "Add PinRec rectangles on layer (1, 10), inset into the waveguide so the PinRec is fully inside Si (1/0).",
        },
        {
            "title": "Scenario 2: Wrong GC Pitch",
            "description": "Layout passes DRC but fails DFT validation on the probe station.",
            "image_desc": "Two grating couplers are 100 µm apart instead of 127 µm.",
            "error": "Grating couplers not on 127 µm pitch",
            "fix": "Adjust GC Y positions so adjacent GCs are exactly 127 µm apart.",
        },
        {
            "title": "Scenario 3: DevRec Overlap",
            "description": "CI reports 'Devices cannot be overlapping' error.",
            "image_desc": "Two components placed too close, their DevRec boxes intersect.",
            "error": "DevRec layers from different components overlap",
            "fix": "Move components apart so DevRec boxes don't touch.",
        },
        {
            "title": "Scenario 4: Out of Floorplan",
            "description": "DRC reports 'devices are out of boundary'.",
            "image_desc": "Part of the waveguide routing extends beyond the floorplan rectangle.",
            "error": "Layout extends outside floorplan layer (99/0)",
            "fix": "Either move the design inside the floorplan or expand the floorplan boundary.",
        },
    ]

    scenario_cards = []
    for scenario in error_scenarios:
        card = doc_callout_html(
            "exercise",
            tag="Exercise",
            title=scenario["title"],
            html=f"""
<p><strong>Situation:</strong> {scenario["description"]}</p>
<p><em>Visual clue:</em> {scenario["image_desc"]}</p>
<details>
<summary style="cursor: pointer; color: #1976d2;"><strong>Click to reveal the error and fix</strong></summary>
<p style="margin-top: 8px;"><strong>Error:</strong> {scenario["error"]}</p>
<p><strong>Fix:</strong> {scenario["fix"]}</p>
</details>
""",
        )
        scenario_cards.append(card)

    mo.vstack(scenario_cards)
    return card, error_scenarios, scenario, scenario_cards


@app.cell
def _(doc_callout_html, mo, show_exercises):
    mo.stop(not show_exercises)

    mo.md("### CI Failure Debugger")

    # Common CI failures and their fixes
    ci_failures = [
        {
            "error_msg": "Error: Devices cannot be overlapping",
            "cause": "Two or more DevRec (68/0) polygons intersect",
            "debug": "Open the .lyrdb file in KLayout → View → Results Browser to see overlap locations",
            "fix": "Increase spacing between components so DevRec boxes don't touch",
        },
        {
            "error_msg": "Error: devices are out of boundary",
            "cause": "Si or SiN layer geometry extends outside Floorplan (99/0) layer",
            "debug": "Check if any routing or components are outside the floorplan rectangle",
            "fix": "Either move design inside floorplan or add/expand the Floorplan layer",
        },
        {
            "error_msg": "Warning: Possible waveguide mismatch or waveguide disconnect",
            "cause": "PinRec marker doesn't enclose exactly one waveguide material",
            "debug": "Check PinRec rectangles on layer (1/10) — they must overlap Si or SiN",
            "fix": "Ensure each PinRec rectangle is centered on a waveguide port and covers only one material",
        },
        {
            "error_msg": "Si minimum feature size violation",
            "cause": "A waveguide or feature is narrower than 70 nm",
            "debug": "Check waveguide widths, especially at bends or tapers",
            "fix": "Increase feature width to at least 70 nm; adjust taper endpoints",
        },
        {
            "error_msg": "Si minimum space violation",
            "cause": "Two Si features are closer than 70 nm apart",
            "debug": "Look for narrow gaps between waveguides or at directional coupler gaps",
            "fix": "Increase gap to at least 70 nm; this may require adjusting coupler design",
        },
        {
            "error_msg": "Multiple top cells found",
            "cause": "GDS file has more than one cell that isn't instantiated by another cell",
            "debug": "Check the cell hierarchy in KLayout",
            "fix": "Ensure only one top-level cell; remove or nest orphan cells",
        },
    ]

    failure_rows = ""
    for failure in ci_failures:
        failure_rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd; vertical-align: top;">
                <code style="color: #d32f2f;">{failure["error_msg"]}</code>
            </td>
            <td style="padding: 8px; border: 1px solid #ddd; vertical-align: top;">
                {failure["cause"]}
            </td>
            <td style="padding: 8px; border: 1px solid #ddd; vertical-align: top;">
                {failure["debug"]}
            </td>
            <td style="padding: 8px; border: 1px solid #ddd; vertical-align: top;">
                {failure["fix"]}
            </td>
        </tr>
        """

    failure_table = f"""
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
        <thead>
            <tr style="background: #ffebee;">
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left; width: 25%;">Error Message</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left; width: 25%;">Root Cause</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left; width: 25%;">How to Debug</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left; width: 25%;">Fix</th>
            </tr>
        </thead>
        <tbody>
            {failure_rows}
        </tbody>
    </table>
    """

    mo.md(f"#### Common CI Failures Reference\n\n{failure_table}")
    return ci_failures, failure, failure_rows, failure_table


# ============================================================================
# SECTION: KLayout Integration Guide
# ============================================================================


@app.cell
def _(mo, show_klayout):
    mo.stop(not show_klayout)
    mo.md(r"""
    <a id="klayout-guide"></a>
    ## KLayout Integration Guide

    Step-by-step instructions for using KLayout with the SiEPIC-EBeam PDK
    for verification.
    """)
    return


@app.cell
def _(doc_callout_list, mo, show_klayout):
    mo.stop(not show_klayout)

    setup_guide = doc_callout_list(
        "info",
        tag="Setup",
        title="First-time KLayout + SiEPIC setup",
        ordered=True,
        items=[
            "Download and install KLayout from <a href='https://www.klayout.de/build.html'>klayout.de</a>",
            "Open KLayout → Tools → Manage Packages",
            "Search for 'SiEPIC' and install the SiEPIC-EBeam package",
            "Restart KLayout after installation",
            "Verify: you should see 'SiEPIC' in the menu bar",
        ],
    )

    verification_guide = doc_callout_list(
        "info",
        tag="Verification",
        title="Running verification in KLayout",
        ordered=True,
        items=[
            "Open your GDS file: File → Open",
            "Load the EBeam technology: SiEPIC → Technology → Load EBeam",
            "Press <strong>V</strong> on your keyboard (or SiEPIC → Verification → Layout Check)",
            "Review any error markers that appear on the layout",
            "For detailed DRC: SiEPIC → Verification → DRC (batch)",
        ],
    )

    results_guide = doc_callout_list(
        "info",
        tag="Results",
        title="Interpreting verification results",
        items=[
            "<strong>Error markers</strong>: Colored shapes highlighting problem areas on the layout",
            "<strong>.lyrdb files</strong>: XML reports listing all DRC violations by category",
            "<strong>Results Browser</strong>: View → Results Browser to navigate errors",
            "Double-click an error in the Results Browser to zoom to that location",
            "The error description tells you what rule was violated",
        ],
    )

    tips_guide = doc_callout_list(
        "warning",
        tag="Tips",
        title="Common pitfalls and tips",
        items=[
            "Make sure you have the correct technology loaded (EBeam) before running verification",
            "If verification seems to do nothing, check that your design is in the active cell",
            "Some warnings (like 'unconnected pins') may be intentional — review each one",
            "Download CI artifacts from GitHub Actions to debug remote failures locally",
            "Keep a clean layout: avoid overlapping text, extra polygons, or orphan cells",
        ],
    )

    mo.vstack([setup_guide, verification_guide, results_guide, tips_guide])
    return results_guide, setup_guide, tips_guide, verification_guide


@app.cell
def _(mo, show_klayout):
    mo.stop(not show_klayout)

    show_advanced_layers = mo.ui.checkbox(
        label="Show advanced layers (SiN, metals)",
        value=False,
    )

    show_advanced_layers
    return (show_advanced_layers,)


@app.cell
def _(doc_callout_html, mo, show_advanced_layers, show_klayout):
    mo.stop(not show_klayout)

    # Quick reference for layer numbers (Si-only focus by default)
    _base_rows = """
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(1, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Si</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Silicon waveguides</td>
                <td style="padding: 8px; border: 1px solid #ddd;">DRC width/space checks</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(1, 10)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">PinRec</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Port markers</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Connectivity check</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(10, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Text</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Labels (opt_in, etc.)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">DFT label check</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(68, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">DevRec</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Device recognition</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Overlap check</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(99, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Floorplan</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Chip boundary</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Boundary check</td>
            </tr>
    """

    _advanced_rows = """
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(4, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">SiN</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Silicon nitride</td>
                <td style="padding: 8px; border: 1px solid #ddd;">DRC width/space checks</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(11, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">M1</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Heater metal</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Metal width/space checks</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(12, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">M2</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Routing metal</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Metal width/space checks</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">(13, 0)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">MLOpen</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Pad opening</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Metal width/space checks</td>
            </tr>
    """

    layer_reference = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 8px;">
        <thead>
            <tr style="background: #e8f5e9;">
                <th style="padding: 8px; border: 1px solid #ddd;">Layer</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Name</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Purpose</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Verification Role</th>
            </tr>
        </thead>
        <tbody>
    """
    layer_reference += _base_rows
    if show_advanced_layers.value:
        layer_reference += _advanced_rows
    layer_reference += """
        </tbody>
    </table>
    """

    layer_callout = doc_callout_html(
        "info",
        tag="Reference",
        title="Layer quick reference for verification",
        html=layer_reference,
    )

    layer_callout
    return (layer_reference,)


@app.cell
def _(mo, show_klayout):
    mo.stop(not show_klayout)
    mo.md(r"""
    ### What's Next

    - **Week 4**: Advanced layout techniques and routing discipline
    - **Homework**: Implement the verification workflow on your own MZI design
    - **Resources**:
        - [SiEPIC-EBeam PDK Documentation](https://github.com/SiEPIC/SiEPIC_EBeam_PDK)
        - [KLayout User Manual](https://www.klayout.de/doc/manual/index.html)
        - DFT rules: `SiEPIC_EBeam_PDK/klayout/EBeam/DFT.xml`
        - DRC deck: `marimo_course/scripts/SiEPIC_EBeam_batch.drc`

    **Suggested homework structure:**
    - Run verification on your Week 2 MZI layout
    - Document any errors found and how you fixed them
    - Attach screenshots of your "green" CI checks
    """)
    return


if __name__ == "__main__":
    app.run()
