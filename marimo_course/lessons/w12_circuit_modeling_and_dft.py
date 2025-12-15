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
        # Week 12 – Circuit Modeling and Design for Test (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 12.
        </div>

        ## Goals
        - Compact models, S-parameters, and “wiring” photonic building blocks into circuits.
        - How PDK components map to circuit models (and where models break).
        - Design-for-test patterns: reference structures, calibration, sweep strategy.

        ## In-class checklist
        - [ ] Explain what an S-parameter is (in words).
        - [ ] List 3 reference structures you’d include on a test chip (and why).
        - [ ] Identify a likely confounder in a photonic measurement and how to control it.

        ## Notes / TODO
        - Add a small circuit-modeling exercise using the same parameters as Week 2.
        """
    )


if __name__ == "__main__":
    app.run()

