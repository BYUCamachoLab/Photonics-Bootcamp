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
        # Week 13 – Measurement and Parameter Extraction I (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 13.
        </div>

        ## Goals
        - Understand the measurement data format used for the run (files, metadata, units).
        - Extract basic MZI metrics: insertion loss (IL), extinction ratio (ER), FSR.
        - Compare measured vs predicted behavior; identify likely causes of mismatch.

        ## In-class checklist
        - [ ] Load one dataset and plot transmission vs wavelength.
        - [ ] Compute FSR and compare to your ΔL-based prediction.
        - [ ] Estimate IL and ER for your device.

        ## Notes / TODO
        - Add a dataset loader + plotting utilities.
        - Add a robust “find peaks/valleys” function for FSR extraction.
        """
    )


if __name__ == "__main__":
    app.run()

