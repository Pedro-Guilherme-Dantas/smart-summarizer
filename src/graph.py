"""Grafo de processamento, independente da origem do texto."""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from .nodes.build_document import build_document
from .nodes.detect_language import make_detect_language_node
from .nodes.summarize import make_summarize_node
from .nodes.translate import make_translate_node
from .state import SummaryState


def route_after_language(state: SummaryState) -> str:
    return "translate" if state["needs_translation"] else "summarize"


def build_graph(model: BaseChatModel):
    builder = StateGraph(SummaryState)
    builder.add_node("detect_language", make_detect_language_node(model))
    builder.add_node("translate", make_translate_node(model))
    builder.add_node("summarize", make_summarize_node(model))
    builder.add_node("build_document", build_document)

    builder.add_edge(START, "detect_language")
    builder.add_conditional_edges(
        "detect_language",
        route_after_language,
        {"translate": "translate", "summarize": "summarize"},
    )
    builder.add_edge("translate", "summarize")
    builder.add_edge("summarize", "build_document")
    builder.add_edge("build_document", END)
    return builder.compile()

