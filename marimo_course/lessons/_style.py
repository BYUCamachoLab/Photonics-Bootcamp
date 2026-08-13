from __future__ import annotations

from textwrap import dedent
from typing import Iterable, Sequence


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _escape_attr(value: str) -> str:
    return _escape_html(value)


def inject_css(mo) -> object:
    return mo.md(
        r"""
        <style>
          :root {
            --doc-max: 920px;
            --doc-muted: color-mix(in srgb, currentColor 65%, transparent);
            --doc-border: color-mix(in srgb, currentColor 18%, transparent);
            --doc-accent: #2563eb;
            --doc-bg: color-mix(in srgb, currentColor 3%, transparent);
          }

          /* "Docs-like" typography + width */
          .markdown.prose,
          .markdown.prose > :is(h1,h2,h3,h4,h5,h6,p,ul,ol,pre,blockquote,table,hr,div) {
            max-width: var(--doc-max);
          }
          .markdown.prose { padding-right: 1rem; }
          .markdown.prose :is(h1,h2,h3) { letter-spacing: -0.01em; }
          .markdown.prose a { color: var(--doc-accent); text-decoration: none; }
          .markdown.prose a:hover { text-decoration: underline; }
          .markdown.prose code {
            background: var(--doc-bg);
            padding: 0.12rem 0.28rem;
            border-radius: 0.3rem;
          }
          .markdown.prose pre code { background: transparent; padding: 0; }
          .markdown.prose pre {
            border: 1px solid var(--doc-border);
            border-radius: 0.7rem;
            padding: 0.9rem 1rem;
            overflow: auto;
          }

          .doc-hero {
            max-width: var(--doc-max);
            border: 1px solid var(--doc-border);
            border-radius: 1rem;
            padding: 1.2rem 1.2rem 0.9rem 1.2rem;
            background: linear-gradient(
              180deg,
              color-mix(in srgb, var(--doc-accent) 10%, transparent),
              transparent
            );
          }
          .doc-hero h1 { margin: 0.2rem 0 0.4rem 0; }
          .doc-hero p { margin: 0.2rem 0 0.8rem 0; color: var(--doc-muted); }
          .doc-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.2rem 0; }
          .doc-badge {
            border: 1px solid var(--doc-border);
            border-radius: 999px;
            padding: 0.15rem 0.55rem;
            font-size: 0.85rem;
            background: color-mix(in srgb, currentColor 2%, transparent);
          }
          .doc-toc {
            max-width: var(--doc-max);
            border: 1px solid var(--doc-border);
            border-radius: 0.9rem;
            padding: 0.8rem 1rem;
            background: color-mix(in srgb, currentColor 1%, transparent);
          }
          .doc-toc ul { margin: 0.4rem 0 0 1.2rem; }

          /* Standard callouts */
          .callout {
            max-width: var(--doc-max);
            border: 1px solid var(--doc-border);
            border-radius: 0.9rem;
            padding: 0.85rem 1rem;
            margin: 0.9rem 0;
            background: color-mix(in srgb, currentColor 1%, transparent);
          }
          .callout-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
          }
          .callout-title .tag {
            font-size: 0.8rem;
            border: 1px solid var(--doc-border);
            border-radius: 999px;
            padding: 0.1rem 0.5rem;
            color: var(--doc-muted);
            font-weight: 600;
          }
          .callout.info { border-left: 5px solid #2563eb; }
          .callout.warning { border-left: 5px solid #b45309; }
          .callout.exercise { border-left: 5px solid #059669; }

          /* Slightly more compact widgets (sliders/buttons/inputs) */
          label, input, select, textarea, button {
            font-size: 0.92rem;
          }

          @media (max-width: 980px) {
            .markdown.prose { padding-right: 1rem; }
          }
        </style>
        """
    )


def _badge_html(label: str) -> str:
    return f'<span class="doc-badge">{_escape_html(label)}</span>'


def doc_badges(
    mo,
    badges: list[str],
    *,
    style: str | None = None,
) -> object:
    style_attr = f' style="{_escape_attr(style)}"' if style else ""
    inner = "".join(_badge_html(b) for b in badges)
    return mo.md(f'<div class="doc-badges"{style_attr}>{inner}</div>')


def doc_callout_list(
    mo,
    kind: str,
    *,
    tag: str,
    title: str,
    items: list[str],
    ordered: bool = False,
    items_are_html: bool = True,
) -> object:
    list_tag = "ol" if ordered else "ul"
    if items_are_html:
        inner = "".join(f"<li>{item}</li>" for item in items)
    else:
        inner = "".join(f"<li>{_escape_html(item)}</li>" for item in items)
    return mo.md(
        dedent(
            f"""
            <div class="callout {kind}">
              <div class="callout-title">
                <span class="tag">{_escape_html(tag)}</span>
                <span>{_escape_html(title)}</span>
              </div>
              <{list_tag}>
                {inner}
              </{list_tag}>
            </div>
            """
        )
    )


def doc_callout_html(
    mo,
    kind: str,
    *,
    tag: str,
    title: str,
    html: str,
) -> object:
    return mo.md(
        dedent(
            f"""
            <div class="callout {kind}">
              <div class="callout-title">
                <span class="tag">{_escape_html(tag)}</span>
                <span>{_escape_html(title)}</span>
              </div>
              {html}
            </div>
            """
        )
    )


def header(
    mo,
    *,
    title: str,
    subtitle: str,
    badges: Sequence[str],
    toc: Iterable[tuple[str, str]],
    build: str | None = None,
) -> object:
    badges_html = "\n".join(_badge_html(b) for b in badges)
    toc_items = "\n".join(
        f'<li><a href="#{_escape_attr(anchor)}">{_escape_html(label)}</a></li>'
        for label, anchor in toc
    )
    build_html = (
        f"<p><small><em>Notebook build: {_escape_html(build)}</em></small></p>"
        if build
        else ""
    )

    hero = f"""
    <div class="doc-hero">
      <div class="doc-badges">
        {badges_html}
      </div>
      <h1>{_escape_html(title)}</h1>
      <p>{_escape_html(subtitle)}</p>
      {build_html}
    </div>
    """

    toc_html = f"""
    <div class="doc-toc">
      <strong>On this page</strong>
      <ul>
        {toc_items}
      </ul>
    </div>
    """

    # Dedent to avoid markdown treating the HTML as a code block.
    return mo.vstack([mo.md(dedent(hero).strip()), mo.md(dedent(toc_html).strip())])
