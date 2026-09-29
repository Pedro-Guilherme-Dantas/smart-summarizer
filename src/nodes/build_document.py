"""Finaliza o Markdown antes da renderização em PDF."""

from ..services import markdown_document
from ..state import SummaryState


def build_document(state: SummaryState) -> dict:
    return {
        "document_markdown": markdown_document.prepare_markdown(
            state["summary_markdown"]
        )
    }

