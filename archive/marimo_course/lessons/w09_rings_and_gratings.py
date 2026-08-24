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
        # Week 9 – Rings and Gratings (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 9.
        </div>

        ## Goals
        - Ring resonators: resonance condition, FSR, Q, coupling regimes.
        - Bragg gratings: reflection, stopband, and design knobs.
        - Compare “interferometer fringes” (MZI) vs “resonances” (rings) conceptually.

        ## In-class checklist
        - [ ] Compute ring FSR from radius (conceptually).
        - [ ] Explain under/critical/over coupling in one sentence each.
        - [ ] Identify a use case where a ring is better than an MZI (and vice versa).

        ## Notes / TODO
        - Add toy models for ring transmission and Bragg reflection.
        """
    )


if __name__ == "__main__":
    app.run()

