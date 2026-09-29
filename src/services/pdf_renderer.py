"""Converte Markdown em PDF usando um layout estável."""

from io import BytesIO

import bleach
from markdown_it import MarkdownIt
from xhtml2pdf import pisa


_ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "em",
    "blockquote", "pre", "code", "br", "hr",
]

_STYLE = """
@page { size: A4; margin: 2cm; }
body { font-family: Helvetica; font-size: 10pt; color: #202124; line-height: 1.4; }
h1 { font-size: 20pt; color: #172554; margin-bottom: 16pt; }
h2 { font-size: 13pt; color: #1e3a8a; margin-top: 14pt; margin-bottom: 7pt; }
h3 { font-size: 11pt; color: #1e3a8a; margin-top: 11pt; }
p { margin-bottom: 8pt; }
ul { list-style-type: none; margin-left: 16pt; }
li { margin-bottom: 4pt; }
blockquote { color: #475569; margin-left: 12pt; }
"""


def render_pdf(markdown: str) -> bytes:
    renderer = MarkdownIt("commonmark", {"html": False, "linkify": False})
    rendered_html = renderer.render(markdown)
    safe_html = bleach.clean(
        rendered_html,
        tags=_ALLOWED_TAGS,
        attributes={},
        strip=True,
    )
    safe_html = safe_html.replace("<li>", "<li>- ")
    html = (
        '<html><head><meta charset="utf-8" />'
        f"<style>{_STYLE}</style></head><body>{safe_html}</body></html>"
    )

    output = BytesIO()
    result = pisa.CreatePDF(html, dest=output, encoding="utf-8", raise_exception=False)
    pdf = output.getvalue()
    if result.err or not pdf.startswith(b"%PDF"):
        raise RuntimeError("Não foi possível gerar o PDF")
    return pdf

