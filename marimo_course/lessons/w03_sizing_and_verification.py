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
    return mo.md(
        r"""
        <style>
        .pb-callout {
          border-left: 4px solid rgba(31, 111, 235, 0.9);
          background: rgba(31, 111, 235, 0.08);
          padding: 10px 12px;
          border-radius: 10px;
          margin: 12px 0;
        }
        .pb-muted { opacity: 0.85; }
        </style>
        """
    )


@app.cell
def _(mo):
    return mo.md(
        r"""
        # Week 3 – Sizing and Verifying the MZI (placeholder)

        <div class="pb-callout">
        This is a placeholder lesson for Week 3. Add narrative, code, and exercises as the course evolves.
        </div>

        ## Goals
        - Choose a target FSR and translate it into a layout ΔL.
        - Pick reasonable splitter/combiner choices (Y-branch vs coupler) for openEBL.
        - Run basic verification checks (DRC-ish sanity, connectivity, labels/pins).

        ## In-class checklist
        - [ ] Compute/confirm target ΔL for your desired FSR.
        - [ ] Update your MZI layout to implement ΔL.
        - [ ] Verify ports/pins/devrec conventions expected by the run repo.

        ## Notes / TODO
        - Add links to openEBL verification steps and CI expectations.
        - Add an example “verification checklist” (what to check in KLayout).
        """
    )


if __name__ == "__main__":
    app.run()

