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
        # Week 8 – Passive Building Blocks I (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 8.
        </div>

        ## Goals
        - Directional couplers and Y-branches: key parameters and behavior.
        - Bandwidth and fabrication sensitivity intuition.
        - Revisit the student MZI design choices through the lens of these components.

        ## In-class checklist
        - [ ] Explain what sets coupler splitting ratio.
        - [ ] Describe how coupler errors affect MZI extinction ratio.
        - [ ] Identify which building block your design used (and why).

        ## Notes / TODO
        - Add a small exercise comparing ideal 50/50 vs imbalanced couplers in an MZI.
        """
    )


if __name__ == "__main__":
    app.run()

