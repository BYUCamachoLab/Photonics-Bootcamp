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
        # Week 4 – Routing and Floorplanning (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 4.
        </div>

        ## Goals
        - Understand footprint trade-offs (bends, spacing, routing length).
        - Make a clean top-level floorplan consistent with openEBL expectations.
        - Keep routing choices consistent with optical testing (I/O placement, straight sections).

        ## In-class checklist
        - [ ] Place I/O structures and decide on a tidy floorplan.
        - [ ] Route the MZI arms cleanly and minimize avoidable loss.
        - [ ] Add/verify labels for device name / metadata (as required).

        ## Notes / TODO
        - Add recommended routing rules-of-thumb and a “common pitfalls” section.
        - Add example screenshots (good vs bad floorplan).
        """
    )


if __name__ == "__main__":
    app.run()

