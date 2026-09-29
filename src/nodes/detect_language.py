"""Classifica o idioma e prepara os trechos de entrada."""

from langchain_core.language_models.chat_models import BaseChatModel

from ..prompts import language
from ..schemas import LanguageDecision
from ..services.text_splitter import sample_for_language, split_text
from ..state import SummaryState


def make_detect_language_node(model: BaseChatModel):
    classifier = model.with_structured_output(
        LanguageDecision.model_json_schema(), method="json_schema"
    )

    async def detect_language(state: SummaryState) -> dict:
        response = await classifier.ainvoke(
            [
                ("system", language.SYSTEM_PROMPT),
                ("human", sample_for_language(state["source_text"])),
            ]
        )
        decision = LanguageDecision.model_validate(response)
        return {
            "chunks": split_text(state["source_text"]),
            "detected_language": decision.detected_language,
            "needs_translation": decision.needs_translation,
        }

    return detect_language

