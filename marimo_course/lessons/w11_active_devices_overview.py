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
        # Week 11 – Active Devices Overview (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 11.
        </div>

        ## Goals
        - MZI modulators/switches: how phase tuning becomes intensity modulation.
        - Thermo-optic vs carrier-based tuning: trade-offs.
        - High-level view of detectors and sources (what’s inside/outside silicon photonics).

        ## In-class checklist
        - [ ] Define Vπ·L and what it means physically.
        - [ ] Explain why thermal tuning is “easy but slow”.
        - [ ] Identify where loss and bandwidth limits come from (qualitatively).

        ## Notes / TODO
        - Add a toy modulator transfer function + bias point exploration.
        """
    )


if __name__ == "__main__":
    app.run()

