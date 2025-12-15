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
        # Week 14 – Measurement and Parameter Extraction II (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 14.
        </div>

        ## Goals
        - Variability and yield: summarize distributions across the class.
        - Sensitivity: connect deviations to likely fabrication/model causes.
        - Build a coherent “design → prediction → measurement → lessons” narrative.

        ## In-class checklist
        - [ ] Compare your extracted ng/neff estimate to references.
        - [ ] Identify the top 2 contributors to mismatch (hypothesis).
        - [ ] Draft 2 plots you’ll use in your final report/presentation.

        ## Notes / TODO
        - Add aggregation across multiple student datasets.
        - Add simple fitting (e.g., sinusoid fit for FSR + phase offset).
        """
    )


if __name__ == "__main__":
    app.run()

