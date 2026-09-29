"""Traduz os trechos quando a decisão do grafo exigir."""

from langchain_core.language_models.chat_models import BaseChatModel

from ..prompts import translation
from ..services.model_text import response_text
from ..state import SummaryState


def make_translate_node(model: BaseChatModel):
    async def translate(state: SummaryState) -> dict:
        translated: list[str] = []
        for chunk in state["chunks"]:
            response = await model.ainvoke(
                [("system", translation.SYSTEM_PROMPT), ("human", chunk)]
            )
            translated.append(response_text(response))
        return {"working_chunks": translated}

    return translate

