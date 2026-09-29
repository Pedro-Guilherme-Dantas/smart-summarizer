"""Dados compartilhados entre as etapas do grafo."""

from typing import NotRequired, TypedDict


class SummaryState(TypedDict):
    source_text: str
    source_label: str
    chunks: NotRequired[list[str]]
    detected_language: NotRequired[str]
    needs_translation: NotRequired[bool]
    working_chunks: NotRequired[list[str]]
    summary_markdown: NotRequired[str]
    document_markdown: NotRequired[str]

