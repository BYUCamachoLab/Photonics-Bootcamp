## ECEN 562 / Photonics Bootcamp – Winter 2026 Course Plan

This document outlines the high-level structure for the Winter 2026 offering, using marimo as the primary environment and targeting submission of a simple MZI design to the SiEPIC openEBL 2026-02 run.

### Key dates
- First class: Wed Jan 7, 2026 (MWF schedule).
- openEBL submission deadline: Sat Feb 14, 2026.
- Expected measurement data return: by late March 2026 (≈ 6 weeks after submission).
- Last class: Wed Apr 15, 2026.

### Phase 1 – Design-first MZI (Jan 7–Feb 14)
- Front-load tooling and design topics so that each student submits at least one simple MZI layout to `openEBL-2026-02` by the deadline.
- Focus on: course orientation, SiEPIC/openEBL overview, environment + PDK setup (KLayout + SiEPIC-EBeam-PDK), basic waveguide and MZI layout, verification (KLayout + GitHub Actions), and submission workflow.
- Use marimo apps for: quick MZI transfer-function visualization, PDK exploration, and simple parameter sweeps that tie layout parameters (ΔL, coupler k, etc.) to expected behavior.

### Phase 2 – Foundations and theory (mid-Feb–late March)
- After submission, rewind and build the theoretical foundations behind the designs, aligned roughly with *Silicon Photonics Design*:
  - Waveguides and materials (Part II, Ch. 3): SOI, effective index, dispersion, bending loss.
  - Passive building blocks (Ch. 4–5): directional couplers, Y-branches, ring resonators, Bragg gratings, optical I/O.
  - Active devices (Part III): modulators, detectors, lasers (as needed for course goals).
- Replace/augment existing Jupyter notebooks with marimo lessons that mix narrative, simulation code, and simple UI controls.

### Phase 3 – System design, fabrication, and parameter extraction (late March–Apr 15)
- Once measurement data for the openEBL run is available, shift to data-driven analysis using student devices:
  - Parameter extraction for MZIs (insertion loss, extinction ratio, FSR, effective index estimates, imbalance).
  - Comparison of predicted vs measured behavior; discussion of fabrication tolerances, model limitations, and packaging/testing effects.
  - Introduction to photonic circuit modeling, PDKs, design-for-test, and simple system-level examples.
- Use marimo notebooks to load and analyze the measurement data, generate plots, and support small group mini-projects based on each student’s design.

### Implementation notes
- The directory `marimo_course/` will contain the new marimo-based course:
  - `marimo_course/index.py`: course “home” app with schedule, links to lessons, and key resources.
  - `marimo_course/lessons/`: one marimo app per major lesson (e.g., `01_intro.py`, `02_mzi_design.py`, `03_waveguides.py`, …).
- The existing Jupyter Book under `book/` is kept as a reference but no longer treated as the primary source for Winter 2026.
- Core modelling and layout tooling is:
  - `marimo` for interactive lessons and analysis.
  - `gdsfactory[full]` for parametric layout and device-level modelling.
  - `simphony` for circuit-level simulation of MZIs and other circuits.
  - KLayout + SiEPIC-EBeam-PDK for PDK-accurate verification and openEBL submission.

## Week-by-week outline (MWF, Fridays as lab)

Winter Semester 2026 runs Jan 7–Apr 15. Classes meet M/W/F, with:
- No class Mon Jan 19 (Martin Luther King Jr. Day).
- No class Mon Feb 16 (Presidents Day).
- Monday-instruction day Tue Feb 17 (follow Monday schedule; this course can meet that day).
- No classes Fri Mar 20 (per BYU calendar).
- Last class on Wed Apr 15 (no Fri meeting that week).

Fridays are reserved as lab/work days (no new core concepts, just guided project/assignment time, ideally in marimo and/or KLayout).

### Week 1 (Jan 7–9) – Orientation and tooling
- Wed: Course overview; silicon photonics fab pipeline; SiEPIC/openEBL 2026-02 goals; high-level MZI design task. Introduce marimo and the local Python environment.
- Fri (lab): Environment setup (Python venv, marimo, gdsfactory, KLayout + SiEPIC-EBeam-PDK), GitHub accounts, and a first marimo MZI demo (play with ΔL and see fringes).

### Week 2 (Jan 12–16) – PDKs and basic MZI layout
- Mon: openEBL process (SOI 220 nm, single full etch); layer table and floorplan. Overview of SiEPIC-EBeam-PDK building blocks (waveguides, couplers, grating couplers).
- Wed: KLayout workflow for creating a simple MZI from PDK cells; intro to DevRec/PinRec, basic routing, and design conventions.
- Fri (lab): Build each student’s first MZI layout skeleton (without strict sizing) and ensure KLayout + PDK tooling runs on their machine.

### Week 3 (Jan 19–23) – Sizing and verifying the MZI
- Mon: No class (MLK Day).
- Wed: Connect layout parameters to behavior: target FSR, ΔL, coupler splitting ratio, expected extinction. Use a marimo analytic MZI app to pick reasonable design targets.
- Fri (lab): Update student MZI layouts to implement chosen ΔL and couplers; run local DRC/verification in KLayout and fix basic errors.

### Week 4 (Jan 26–30) – Ring resonators + adding extra structures
- Mon: Ring resonators (layout-first): resonance condition, FSR, Q, and coupling regimes. Pick a radius and sketch a clean bus + ring floorplan that is easy to probe.
- Wed: Add “interesting structures” to the design: at least one ring (or ring sweep) plus practical test structures (straight/spiral waveguides, references). Emphasize probe-friendly I/O placement and routing discipline.
- Fri (lab): Implement the added structures in layout, keep the floorplan tidy, and ensure the design remains compatible with openEBL conventions and downstream checks.

### Week 5 (Feb 2–6) – GitHub and openEBL checks
- Mon: Git/GitHub workflow for openEBL: forking `openEBL-2026-02`, turning on Actions, and understanding CI status and artifacts.
- Wed: Walkthrough of running checks locally (where feasible) versus relying on GitHub Actions; interpreting common DRC/functional errors.
- Fri (lab): Each student uploads their draft `.gds`/`.oas` (or Python-driven GDS generator), triggers CI, downloads artifacts into KLayout, and fixes any reported issues. Aim for most designs to be “green” by end of week.

### Week 6 (Feb 9–13) – Submission buffer and bridge to theory
- Mon: Final design QA: checklist for manufacturability and testability; ensure each design includes appropriate test structures (e.g., reference waveguides, grating couplers).
- Wed: Last chance to resolve failing CI checks; create/merge Pull Requests to `openEBL-2026-02`. Brief high-level preview of waveguide and interferometer theory to bridge into Phase 2.
- Fri (lab): Submission buffer and troubleshooting clinic; by the end of this day, all students should have successful PRs ahead of the Feb 14 deadline.

### Week 7 (Feb 16–20) – Waveguide fundamentals
- Mon: No class (Presidents Day).
- Tue: Monday-instruction day – start theoretical foundations: SOI materials, index contrast, guided modes, effective index, and simple slab waveguide models (tied back to the waveguides used in their MZIs).
- Wed: Continue waveguide topics (bending loss, dispersion, and practical design rules) and connect back to their MZI layouts.
- Fri (lab): marimo lab exploring mode profiles and effective index vs geometry using available tools (e.g., gdsfactory mode solvers or simplified models).

### Week 8 (Feb 23–27) – Passive building blocks I
- Mon: Directional couplers and Y-branches: qualitative operation, key design parameters (gap, length), bandwidth, and fabrication sensitivity.
- Wed: Mach–Zehnder interferometers as building blocks: revisit their design choices in light of theory; discuss imbalance, excess loss, and phase errors.
- Fri (lab): marimo exercises for simple coupler and MZI models; short design tweaks “what would you change in your submitted design now?”.

### Week 9 (Mar 2–6) – Passive building blocks II: rings and gratings
- Mon: Ring resonators: resonance conditions, FSR, Q, coupling regimes. Relation to MZI behavior and filtering.
- Wed: Waveguide Bragg gratings and reflection-based filters; high-level design knobs and typical applications.
- Fri (lab): marimo lab to experiment with ring/MZI/Bragg toy models (no new concepts, just hands-on parameter exploration).

### Week 10 (Mar 9–13) – Optical I/O and packaging
- Mon: Grating and edge couplers: mode matching, bandwidth, polarization, and trade-offs.
- Wed: Practical packaging and testing considerations: fiber arrays, alignment tolerances, probe stations; what their openEBL chips will actually “see” in the lab.
- Fri (lab): marimo + documentation-focused lab: estimate expected coupling losses and total power budgets for their own MZIs.

### Week 11 (Mar 16–20) – Active devices overview
- Mon: Introduction to modulators (carrier depletion/injection, thermo-optic tuning) and how an MZI becomes an active switch/modulator.
- Wed: Overview of detectors and light sources in silicon photonics; how a future run could expand their passive designs into full links.
- Fri: No class (BYU “No Classes” day). Optionally assign an asynchronous marimo-based lab with parameter sweeps of simple modulator/detector models (e.g., Vπ·L, bandwidth, responsivity) for students to complete outside of class.

### Week 12 (Mar 23–27) – Circuit modeling and design for test
- Mon: Photonic circuit modeling concepts (compact models, S-parameters, simple circuit simulators) and how they relate to PDK components.
- Wed: Design-for-test strategies: reference structures, test coupons, layout considerations to ease probing and interpretation.
- Fri (lab): marimo lab to build simple circuit-level models (e.g., a small network of couplers and phase shifters) and predict measurements similar to what they will receive from openEBL.

### Week 13 (Mar 30–Apr 3) – Measurement and parameter extraction I
- Mon: Once measurement data is available (target: late March), introduce the actual openEBL measurement results format and basic parameter extraction workflows (IL, ER, FSR).
- Wed: Work through example MZI datasets in marimo: fit fringes, extract effective index and ΔL, compare to pre-fab predictions.
- Fri (lab): Students begin analyzing their own device data where available; otherwise use shared example datasets with a similar topology.

### Week 14 (Apr 6–10) – Measurement and parameter extraction II
- Mon: Variability and yield: distributions over student designs, sensitivity to fabrication errors, and what could be improved in a “second tape-out”.
- Wed: Small-group mini-project time: each group frames a short story about their device (design → prediction → measurement → lessons learned).
- Fri (lab): Dedicated project work in marimo: finalize analyses, figures, and short write-ups or presentation materials.

### Week 15 (Apr 13–15) – Wrap-up and reflection
- Mon: Project presentations and/or synthesized discussion of key course themes: from foundry PDKs to layout, fabrication, measurement, and modeling.
- Wed (last class): Course wrap-up, reflection on the design–fab–test cycle, and pointers to further work (research, future runs, and advanced topics). No Friday meeting this week.
