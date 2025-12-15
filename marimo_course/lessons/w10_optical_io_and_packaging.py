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
        # Week 10 – Optical I/O and Packaging (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 10.
        </div>

        ## Goals
        - Grating vs edge couplers: trade-offs and practical constraints.
        - Packaging/testing realities: fiber arrays, alignment, polarization.
        - Power budget thinking: coupling loss + propagation + device excess loss.

        ## In-class checklist
        - [ ] Estimate total insertion loss for your device chain (back-of-the-envelope).
        - [ ] Identify the dominant uncertainty in that estimate.
        - [ ] Explain why polarization management matters for measurement.

        ## Notes / TODO
        - Add a simple power budget worksheet + example numbers.
        """
    )


if __name__ == "__main__":
    app.run()

