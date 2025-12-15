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
        # Week 15 – Wrap-up and Reflection (placeholder)

        <div class="pb-callout">
        Placeholder lesson for Week 15.
        </div>

        ## Goals
        - Synthesize course themes: design → fab → test → model refinement.
        - Reflect on what worked and what you’d change in a second tape-out.
        - Identify next steps (research topics, more advanced tools, future runs).

        ## Reflection prompts
        1. What surprised you most when comparing prediction vs measurement?
        2. If you could change one design decision, what would it be and why?
        3. What measurement or analysis tool would you add for the next run?

        ## Notes / TODO
        - Add links to future resources (papers, tutorials, software).
        - Add a final “course takeaways” checklist.
        """
    )


if __name__ == "__main__":
    app.run()

