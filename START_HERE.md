# Start Here (Students)

## Day 1: Get running quickly (recommended)

1. Clone the course repository
   - `git clone <REPO_URL>`
   - `cd Photonics-Bootcamp`

2. Install prerequisites
   - Python 3.11+
   - `uv` (verify: `uv --version`)
   - `marimo` (verify: `marimo --version`)

3. Open the Week 1 “Orientation + Tooling” lesson in marimo sandbox mode
   - `marimo edit --sandbox marimo_course/lessons/w01_orientation_tooling.py`

4. Then open the practice notebook
   - `marimo edit --sandbox marimo_course/lessons/practice_marimo.py`

## Optional: Use a single local virtual environment instead of sandbox mode

From the repo root (`Photonics-Bootcamp`):

- `python3 -m venv .venv`
- `source .venv/bin/activate`  (Windows PowerShell: `.venv\\Scripts\\Activate.ps1`)
- `pip install -r marimo_course/requirements.txt`
- `marimo edit marimo_course/lessons/w01_orientation_tooling.py`

