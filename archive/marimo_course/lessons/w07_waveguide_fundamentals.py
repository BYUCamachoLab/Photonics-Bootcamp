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
        # Week 7 – Waveguide Fundamentals (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 7.
        </div>

        ## Goals
        - Review guided modes, effective index, and dispersion intuition.
        - Connect group index to MZI FSR and measurement interpretation.
        - Introduce bending loss and practical design rules.

        ## In-class checklist
        - [ ] Define effective index vs group index (in your own words).
        - [ ] Predict how dispersion changes an MZI spectrum.
        - [ ] Identify layout features that increase waveguide loss.

        ## Notes / TODO
        - Add a simple “FSR vs ng” exercise tied to student ΔL values.
        - Add references to the textbook sections used in this week.
        """
    )


if __name__ == "__main__":
    app.run()

