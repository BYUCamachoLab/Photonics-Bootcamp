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
        </style>
        """
    )


@app.cell
def _(mo):
    return mo.md(
        r"""
        # Week 6 – Submission Buffer and Bridge to Theory (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 6.
        </div>

        ## Goals
        - Final submission QA checklist (manufacturability + testability).
        - Lock the design and document parameters for later comparison.
        - Preview the theory arc: waveguides, couplers, MZI modeling, measurement.

        ## In-class checklist
        - [ ] Final PR ready (green CI).
        - [ ] Record your design parameters: ΔL, coupler choice, footprint, expected FSR.
        - [ ] Write down 2–3 hypotheses about expected measurement behavior.

        ## Notes / TODO
        - Add a “submission day” checklist students can follow.
        - Add a short reflection prompt (what you’d change if you had one more week).
        """
    )


if __name__ == "__main__":
    app.run()

