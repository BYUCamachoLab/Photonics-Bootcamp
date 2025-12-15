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
        # Week 5 – Submission Workflow and CI Checks (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 5.
        </div>

        ## Goals
        - Understand the openEBL submission repo structure and expectations.
        - Run local checks before pushing (when possible).
        - Interpret CI failures and iterate quickly.

        ## In-class checklist
        - [ ] Fork/clone the run repo and create a branch for your design.
        - [ ] Place your GDS in the correct path.
        - [ ] Open a PR and confirm CI runs.
        - [ ] Fix at least one CI failure (practice loop).

        ## Notes / TODO
        - Add specific links/commands for the 2026-02 run repo verification.
        - Add a troubleshooting table (“error → likely fix”).
        """
    )


if __name__ == "__main__":
    app.run()

