#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "marimo>=0.18.4",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _(mo):
    from _notebook_template import inject_css

    inject_css(mo)
    return


@app.cell
def _(mo):
    from _notebook_template import make_doc_helpers

    doc_badges, doc_callout_html, doc_callout_list = make_doc_helpers(mo)
    return doc_badges, doc_callout_html, doc_callout_list


@app.cell
def _(mo):
    from _notebook_template import make_section_tabs

    section_view, view_state, set_view = make_section_tabs(mo)
    instructor_mode = mo.ui.checkbox(label="Instructor mode", value=False)
    mo.vstack([section_view, instructor_mode])
    return instructor_mode, set_view, view_state


@app.cell
def _(instructor_mode, view_state):
    view = view_state()
    show_overview = view in ["All", "Overview"]
    show_theory = view in ["All", "Theory"]
    show_interactive = view in ["All", "Interactive"]
    show_layout_section = view in ["All", "Layout"]
    return (
        instructor_mode.value,
        show_interactive,
        show_layout_section,
        show_overview,
        show_theory,
    )


@app.cell
def _(
    doc_badges,
    instructor_mode,
    show_interactive,
    show_layout_section,
    show_overview,
    show_theory,
    view_state,
):
    doc_badges(
        [
            f"View: <strong>{view_state()}</strong>",
            (
                "Flags: "
                f"overview={show_overview}, theory={show_theory}, interactive={show_interactive}, layout={show_layout_section}"
            ),
            f"Instructor mode: <strong>{bool(instructor_mode)}</strong>",
        ]
    )
    return


@app.cell
def _(mo):
    from _notebook_template import make_health_refresh_button

    health_refresh = make_health_refresh_button(mo)
    return health_refresh


@app.cell
def _(doc_callout_html, health_refresh, mo):
    from _notebook_template import safe_editing_panel

    safe_editing_panel(
        mo,
        doc_callout_html,
        health_refresh,
        restore_command="git -C Photonics-Bootcamp restore marimo_course/lessons/<your_notebook>.py",
        external_check_command="python3 marimo_course/lessons/check_notebook_health.py marimo_course/lessons/<your_notebook>.py",
    )
    return


@app.cell
def _(doc_badges, doc_callout_html, health_refresh):
    from _notebook_template import notebook_self_check_view

    _self_check_view = notebook_self_check_view(
        doc_badges=doc_badges,
        doc_callout_html=doc_callout_html,
        notebook_path=__file__,
        refresh_token=health_refresh.value,
    )
    _self_check_view
    return


@app.cell
def _(mo, show_overview):
    mo.stop(not show_overview)
    from _style import header

    header(
        mo,
        title="Lesson title",
        subtitle="1–2 sentence lesson description.",
        badges=["Week X", "Topic", "Tooling"],
        toc=[
            ("Intro", "intro"),
            ("Theory", "theory"),
            ("Interactive", "interactive"),
            ("Layout", "layout"),
        ],
        build="YYYY-MM-DD",
    )
    return


@app.cell
def _(doc_callout_html, mo, show_overview):
    mo.stop(not show_overview)
    doc_callout_html(
        "info",
        tag="Overview",
        title="What students should do",
        html="<ul><li>Replace placeholders.</li><li>Keep compute cells ungated.</li></ul>",
    )
    return


@app.cell
def _(mo, show_theory):
    mo.stop(not show_theory)
    mo.md(
        r"""
        <a id="theory"></a>
        ## Theory

        Put derivations here.
        """
    )
    return


@app.cell
def _(mo, show_interactive):
    mo.stop(not show_interactive)
    mo.md(
        r"""
        <a id="interactive"></a>
        ## Interactive

        Put widgets/plots here.
        """
    )
    return


@app.cell
def _(mo, show_layout_section):
    mo.stop(not show_layout_section)
    mo.md(
        r"""
        <a id="layout"></a>
        ## Layout

        Put layout preview/export here.
        """
    )
    return


if __name__ == "__main__":
    app.run()
