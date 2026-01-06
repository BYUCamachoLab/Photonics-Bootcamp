#!/usr/bin/env python3
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
def _(mo):
    mo.md(r"""
    # Week 1 – Course Orientation and Tooling

    Goals for this lesson:

    - Understand the overall arc of the Winter 2026 course.
    - See the design–fab–test cycle and the role of the openEBL 2026-02 run.
    - Set up the local Python + marimo environment and verify marimo runs.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <style>
    .pb-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin: 10px 0 18px;
    }
    .pb-card {
      border: 1px solid rgba(120, 120, 120, 0.35);
      border-radius: 12px;
      padding: 12px 14px;
      background: rgba(120, 120, 120, 0.06);
    }
    .pb-card h3 {
      margin: 0 0 6px 0;
      font-size: 1.05rem;
    }
    .pb-card pre {
      margin: 8px 0 0;
      padding: 10px 12px;
      border-radius: 10px;
      background: rgba(120, 120, 120, 0.10);
      overflow-x: auto;
    }
    .pb-muted { opacity: 0.85; }
    .pb-callout {
      border-left: 4px solid rgba(31, 111, 235, 0.9);
      background: rgba(31, 111, 235, 0.08);
      padding: 10px 12px;
      border-radius: 10px;
      margin: 12px 0;
    }
    </style>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="toc"></a>
    <div class="pb-callout">
    <strong>Start here (in class):</strong> open the notebook in marimo sandbox mode, then scroll using the Table of Contents.
    <div class="pb-muted" style="margin-top:6px;">
    Tip: run commands from the <code>Photonics-Bootcamp</code> repo root (the folder that contains <code>marimo_course/</code>).
    </div>
    </div>

    <div class="pb-grid">
      <div class="pb-card">
        <h3>Week 1 (this notebook)</h3>
        <div class="pb-muted">Orientation + setup checklist + semester calendar.</div>
        <pre><code>marimo edit --sandbox marimo_course/lessons/w01_orientation_tooling.py</code></pre>
      </div>
      <div class="pb-card">
        <h3>Practice marimo</h3>
        <div class="pb-muted">A short, safe sandbox for UI + reactivity.</div>
        <pre><code>marimo edit --sandbox marimo_course/lessons/practice_marimo.py</code></pre>
      </div>
      <div class="pb-card">
        <h3>Week 2 (MZI modelling)</h3>
        <div class="pb-muted">Interactive MZI transfer functions + Simphony.</div>
        <pre><code>marimo edit --sandbox marimo_course/lessons/w02_mzi_modelling.py</code></pre>
      </div>
    </div>

    ## Table of contents
    - <a href="#resources">Key resources</a>
    - <a href="#calendar">Semester calendar</a>
    - <a href="#setup">Setup checklist</a>
    - <a href="#auto-check">Quick environment check</a>
    - <a href="#commands">Common commands</a>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="resources"></a>
    ## Key resources

    - Photonics-Bootcamp repository (this repo).
    - SiEPIC openEBL 2026-02: https://github.com/SiEPIC/openEBL-2026-02
    - BYU Academic Calendar 2026: https://academiccalendar.byu.edu/?y=2026
    - Textbook: *Silicon Photonics Design* by Chrostowski and Hochberg.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="calendar"></a>
    ## Semester calendar (Winter 2026)

    Key milestones (from `COURSE_PLAN.md`):

    - First class: **Wed Jan 7, 2026**
    - openEBL submission deadline: **Sat Feb 14, 2026**
    - Last class: **Wed Apr 15, 2026**

    Class cadence: **M/W/F** (Fridays are lab/work days). Calendar exceptions:
    - No class **Mon Jan 19** (MLK Day)
    - No class **Mon Feb 16** (Presidents Day)
    - **Tue Feb 17** follows Monday instruction (course can meet)
    - No classes **Fri Mar 20** (BYU calendar)
    """)
    return


@app.cell
def _():
    from datetime import date, timedelta
    return date, timedelta


@app.cell
def _(date, timedelta):
    first_class = date(2026, 1, 7)
    last_class = date(2026, 4, 15)

    # Regular meeting days (Mon/Wed/Fri) plus one special Tuesday meeting.
    meeting_weekdays = {0, 2, 4}  # Mon=0, Wed=2, Fri=4
    monday_instruction_tuesday = date(2026, 2, 17)

    no_class_dates = {
        date(2026, 1, 19),  # MLK Day
        date(2026, 2, 16),  # Presidents Day
        date(2026, 3, 20),  # BYU no-classes day
    }

    week_topics = {
        1: "Orientation and tooling",
        2: "PDKs and basic MZI layout",
        3: "Sizing and verifying the MZI",
        4: "Routing and floorplanning",
        5: "Submission workflow and CI checks",
        6: "Submission buffer and bridge to theory",
        7: "Waveguide fundamentals",
        8: "Passive building blocks I",
        9: "Passive building blocks II: rings and gratings",
        10: "Optical I/O and packaging",
        11: "Active devices overview",
        12: "Circuit modeling and design for test",
        13: "Measurement and parameter extraction I",
        14: "Measurement and parameter extraction II",
        15: "Wrap-up and reflection",
    }

    # Define "Week 1" as the week containing the first class, starting Monday.
    week1_monday = first_class - timedelta(days=first_class.weekday())

    rows = []
    d = week1_monday
    while d <= last_class:
        is_regular_meeting = d.weekday() in meeting_weekdays
        is_special_meeting = d == monday_instruction_tuesday
        if is_regular_meeting or is_special_meeting:
            status = "No class" if d in no_class_dates else "Meets"
            if is_special_meeting:
                day_label = "Tue"
                meeting_type = "Lecture (Mon schedule)"
            else:
                day_label = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d.weekday()]
                meeting_type = "Lab" if d.weekday() == 4 else "Lecture"

            week = 1 + ((d - week1_monday).days // 7)
            rows.append(
                {
                    "week": week,
                    "date": d.isoformat(),
                    "day": day_label,
                    "type": meeting_type,
                    "status": status,
                    "week_topic": week_topics.get(week, ""),
                }
            )
        d += timedelta(days=1)

    max_week = max(r["week"] for r in rows)
    return max_week, rows


@app.cell
def _(max_week, mo):
    week_selector = mo.ui.slider(start=1, stop=max_week, step=1, value=1, label="Week")
    mo.vstack([mo.md("### Calendar controls"), week_selector])
    return (week_selector,)


@app.cell
def _(mo, rows, week_selector):
    selected = [r for r in rows if r["week"] == week_selector.value]
    topic = next((r["week_topic"] for r in selected if r["week_topic"]), "")

    blocks = [
        mo.md("### Weekly view"),
        mo.ui.table(selected),
    ]
    if topic:
        blocks.insert(1, mo.md(f"Week {week_selector.value}: **{topic}**"))
    blocks.extend([mo.md("### Full list (sortable)"), mo.ui.table(rows)])
    blocks.append(mo.md(r"""<a href="#toc">Back to top</a>"""))
    mo.vstack(blocks)
    return


@app.cell
def _(mo):
    mo.md(r"""
    <a id="setup"></a>
    ## Environment checklist (to verify in class)

    - Python 3.11+ installed.
    - Virtual environment created in the course repo.
    - `marimo` installed and `marimo edit` works.
    - `gdsfactory[full]` installed and importable (e.g., `import gdsfactory as gf`).
    - `simphony` installed and importable.
    - KLayout + SiEPIC-EBeam-PDK installed and able to open example layouts.

    In this lesson, we will walk through these steps and ensure everyone can run the course materials.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Two ways to run this course (sandbox vs local venv)

    You have two supported workflows:

    ### Option A — marimo sandbox mode (recommended for most students)

    Run notebooks in an isolated `uv` environment using the notebook’s inline dependency metadata.

    - **How**: `marimo edit --sandbox <notebook.py>` or `marimo run --sandbox <notebook.py>`
    - **Requirements**:
      - `uv` installed (`uv --version`)
      - Python 3.11+
    - **Pros**:
      - Reproducible per-notebook environments
      - Minimal “global” setup; avoids dependency conflicts
      - Easy to reset by deleting the sandbox environment cache
    - **Cons**:
      - First run can be slower while dependencies install
      - Environments are per-notebook (can duplicate installs)
      - Some system-level tools (KLayout/PDKs) are still manual

    ### Option B — local virtual environment (recommended for power users)

    Create one course environment and run all notebooks inside it.

    - **Requirements**:
      - Python 3.11+ and `pip`
      - Ability to create venvs (`python -m venv`)
      - Install course packages: `pip install -r marimo_course/requirements.txt`
    - **Pros**:
      - One environment for the whole course (faster day-to-day)
      - Easier to integrate additional tools and packages
      - Better if you want to tinker beyond the notebook’s pinned deps
    - **Cons**:
      - More setup up-front
      - Possible version conflicts (especially with photonics tooling stacks)
    """)
    return


@app.cell
def _(mo):
    has_python = mo.ui.checkbox(label="Python 3.11+ installed", value=False)
    has_venv = mo.ui.checkbox(label="Virtual environment created + activated", value=False)
    has_marimo = mo.ui.checkbox(label="marimo installed; `marimo edit` works", value=False)
    has_gdsfactory = mo.ui.checkbox(label="gdsfactory import works", value=False)
    has_simphony = mo.ui.checkbox(label="simphony import works", value=False)
    has_klayout = mo.ui.checkbox(
        label="KLayout + SiEPIC-EBeam-PDK installed (manual check)", value=False
    )
    return (
        has_gdsfactory,
        has_klayout,
        has_marimo,
        has_python,
        has_simphony,
        has_venv,
    )


@app.cell
def _(
    has_gdsfactory,
    has_klayout,
    has_marimo,
    has_python,
    has_simphony,
    has_venv,
    mo,
):
    mo.md("## Setup progress (interactive)")

    checks = [
        has_python,
        has_venv,
        has_marimo,
        has_gdsfactory,
        has_simphony,
        has_klayout,
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

    mo.vstack(
        [
            has_python,
            has_venv,
            has_marimo,
            has_gdsfactory,
            has_simphony,
            has_klayout,
            mo.md(f"Progress: **{completed}/{len(checks)}** completed."),
            mo.md(progress_bar),
            mo.md(r"""<a href="#toc">Back to top</a>"""),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    <a id="auto-check"></a>
    ## Quick environment check (automatic)
    """)
    return


@app.cell
def _():
    import sys
    from importlib import metadata
    return metadata, sys


@app.cell
def _(metadata, mo, sys):
    def version_of(package: str) -> str | None:
        try:
            return metadata.version(package)
        except metadata.PackageNotFoundError:
            return None

    python_ok = (sys.version_info.major, sys.version_info.minor) >= (3, 11)
    python_status = "OK" if python_ok else "NEEDS 3.11+"

    import platform
    import shutil

    uv_path = shutil.which("uv")
    marimo_path = shutil.which("marimo")

    packages = [
        ("marimo", version_of("marimo")),
        ("pyzmq", version_of("pyzmq")),
        # These are used in later lessons; they may be missing in Week 1 sandbox mode.
        ("gdsfactory", version_of("gdsfactory")),
        ("simphony", version_of("simphony")),
        ("altair", version_of("altair")),
        ("polars", version_of("polars")),
        ("numpy", version_of("numpy")),
    ]

    package_rows = []
    for name, version in packages:
        package_rows.append(
            {
                "package": name,
                "status": "OK" if version is not None else "MISSING",
                "version": version or "",
            }
        )

    header = mo.md(
        "Python: "
        + f"`{sys.version.split()[0]}`"
        + f" (check: **{python_status}**)\n\n"
        + f"Executable: `{sys.executable}`  \n"
        + f"Platform: `{platform.system()} {platform.release()}`\n\n"
        + f"`uv` on PATH: **{'YES' if uv_path else 'NO'}**"
        + (f" (`{uv_path}`)" if uv_path else "")
        + "  \n"
        + f"`marimo` on PATH: **{'YES' if marimo_path else 'NO'}**"
        + (f" (`{marimo_path}`)" if marimo_path else "")
        + "\n\n"
        + "Installed packages (from Python environment running this notebook):"
    )
    table = mo.ui.table(package_rows)
    mo.vstack(
        [
            header,
            table,
            mo.md(
                r"""
                <div class="pb-muted">
                Note: if you are running this notebook in <code>--sandbox</code> mode, only the packages listed in this file’s inline metadata are expected.
                Later notebooks include additional dependencies via their inline metadata (or via your course-wide venv).
                </div>
                """
            ),
            mo.md(r"""<a href="#toc">Back to top</a>"""),
        ]
    )
    return


@app.cell
def _(mo):
    platform_choice = mo.ui.radio(
        options={
            "macOS / Linux": "unix",
            "Windows (PowerShell)": "win",
        },
        value="macOS / Linux",
        label="Platform",
    )
    mo.vstack([mo.md('<a id="commands"></a>\n## Common commands'), platform_choice])
    return (platform_choice,)


@app.cell
def _(mo, platform_choice):
    if platform_choice.value == "win":
        local = mo.md(
            r"""
            **Local venv (course-wide):**
            ```powershell
            py -3 -m venv .venv
            .venv\Scripts\Activate.ps1
            pip install -r marimo_course/requirements.txt
            ```
            """
        )
    else:
        local = mo.md(
            r"""
            **Local venv (course-wide):**
            ```bash
            python3 -m venv .venv
            source .venv/bin/activate
            pip install -r marimo_course/requirements.txt
            ```
            """
        )

    sandbox = mo.md(
        r"""
        **Sandbox mode (per-notebook, recommended):**
        ```bash
        marimo edit --sandbox marimo_course/lessons/w01_orientation_tooling.py
        ```
        """
    )

    mo.vstack([local, sandbox, mo.md(r"""<a href="#toc">Back to top</a>""")])
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
