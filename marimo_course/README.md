## `marimo_course/` – Winter 2026 marimo-based course

This directory will contain the marimo-first version of the Photonics Bootcamp / ECEN 562 course for Winter 2026.

Planned structure:
- `index.py`: marimo “course home” app (schedule, links to lessons, key deadlines such as the openEBL submission date).
- `lessons/`: marimo lesson files (one per topic or class meeting), replacing the old Jupyter notebooks as the canonical source.

Tooling for the marimo course (students):
- Python 3.11+ with a course virtual environment.
- `marimo` for notebooks/apps (this repo currently targets **marimo 0.18.4**; using a very different marimo version to *edit/save* notebooks can sometimes corrupt exports).
- `gdsfactory[full]` for parametric layout and device-level modelling.
- `simphony` for circuit-level modelling and simulation.
- KLayout + SiEPIC-EBeam-PDK for verification and final openEBL layout checks.

The high-level plan and timeline are documented in `COURSE_PLAN.md` at the repo root.

## Setup instructions (local environment)

From the repository root (`Photonics-Bootcamp`):

## Option A: marimo sandbox mode (recommended for students)

Run each lesson in an isolated `uv` environment using PEP 723 inline metadata (no manual `pip install` needed for lessons that declare dependencies).

Examples:
- Edit Week 1 lesson: `marimo edit --sandbox marimo_course/lessons/w01_orientation_tooling.py`
- Edit practice sandbox: `marimo edit --sandbox marimo_course/lessons/practice_marimo.py`
- Run Week 2 modelling as an app: `marimo run --sandbox marimo_course/lessons/w02_mzi_modelling.py`

Notes:
- Requires `uv` installed (`uv --version`).
- The first run may take a few minutes while dependencies install.

## Editing safety (recommended)

Marimo notebooks can become corrupted if saved/exported with an incompatible marimo version; the symptom is usually `app._unparsable_cell(...)` and errors like `SyntaxError: 'return' outside function`.

After editing a lesson:
- Run `marimo check marimo_course/lessons/<lesson>.py`
- Run `python3 marimo_course/lessons/check_notebook_health.py marimo_course/lessons/<lesson>.py`

If a lesson gets corrupted:
- Recover with `git -C Photonics-Bootcamp restore marimo_course/lessons/<lesson>.py`
- Restart marimo

## Option B: course virtual environment (instructor / power users)

1. Create and activate a virtual environment
   - macOS / Linux:
     - `python3 -m venv .venv`
     - `source .venv/bin/activate`
   - Windows (PowerShell):
     - `py -3 -m venv .venv`
     - `.venv\Scripts\Activate.ps1`

2. Install Python dependencies for the marimo course
   - `pip install -r marimo_course/requirements.txt`

3. Verify imports
   - In Python (inside the venv), run:
     - `import marimo as mo`
     - `import gdsfactory as gf`
     - `import simphony`

4. Run the marimo course home page
   - From the repo root with the venv active:
     - `marimo edit marimo_course/index.py`

5. Install KLayout + SiEPIC-EBeam-PDK
   - Follow the SiEPIC-EBeam-PDK installation instructions linked from the openEBL README.
   - Verify that KLayout opens and that you can load example layouts from the PDK.
