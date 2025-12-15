import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # ECEN 562 / Photonics Bootcamp – Winter 2026

    This marimo app serves as the course home page for the Winter 2026 marimo-based version of the class.

    **Key dates**

    - First class: **Wed Jan 7, 2026**
    - openEBL submission (simple MZI design): **Sat Feb 14, 2026**
    - Expected measurement results available: **late March 2026**
    - Last class: **Wed Apr 15, 2026**

    **Structure**

    - Phase 1 (Weeks 1–6): Design-first MZI and openEBL submission
    - Phase 2 (Weeks 7–12): Waveguides, passive/active components, I/O, and circuit modeling
    - Phase 3 (Weeks 13–15): Measurement analysis and parameter extraction using student devices
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Weekly overview

    - **Week 1 (Jan 7–9)** – Orientation and tooling
      Course overview, SiEPIC/openEBL 2026-02, environment setup, and first marimo MZI demo.

    - **Week 2 (Jan 12–16)** – PDKs and basic MZI layout
      openEBL process, SiEPIC-EBeam-PDK, and first MZI layout skeleton in KLayout.

    - **Week 3 (Jan 19–23)** – Sizing and verifying the MZI
      Connect layout parameters to behavior; local DRC/verification in KLayout.

    - **Week 4 (Jan 26–30)** – Towards manufacturable designs
      Layout polishing, floorplans, DevRec/PinRec, and verification concepts.

    - **Week 5 (Feb 2–6)** – GitHub and openEBL checks
      Forking `openEBL-2026-02`, CI checks, and artifact-based debugging.

    - **Week 6 (Feb 9–13)** – Submission buffer and bridge to theory
      Final design QA and openEBL submissions; preview of waveguide/interferometer theory.

    - **Weeks 7–12** – Foundations and theory
      Waveguides, passive building blocks, rings/Bragg gratings, optical I/O, active devices, and circuit modeling.

    - **Weeks 13–15** – Measurements and parameter extraction
      Analyze openEBL measurement data, extract parameters, and present design–fab–test results.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Lesson links (to be filled in)

    As marimo lessons are created, links will be added here. Planned structure:

    - `lessons/w01_orientation_tooling.py` – Course overview, openEBL goals, and environment setup.
    - `lessons/w02_pdk_mzi_layout.py` – PDK and first MZI layout.
    - `lessons/w02_mzi_modelling.py` – Analytic / simulated MZI model and design targets.
    - `lessons/w03_verification_and_github.py` – Verification workflow and GitHub CI.
    - Additional lessons for theory and measurement analysis in later weeks.
    """)
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
