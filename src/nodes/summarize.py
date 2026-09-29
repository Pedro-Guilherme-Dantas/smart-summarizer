"""Resume os trechos e consolida um documento único."""

from langchain_core.language_models.chat_models import BaseChatModel

from ..prompts import summary
from ..services.model_text import response_text
from ..state import SummaryState


def make_summarize_node(model: BaseChatModel):
    async def summarize(state: SummaryState) -> dict:
        chunks = state.get("working_chunks", state["chunks"])
        if len(chunks) == 1:
            response = await model.ainvoke(
                [("system", summary.SINGLE_PROMPT), ("human", chunks[0])]
            )
            return {"summary_markdown": response_text(response)}

        partials: list[str] = []
        for index, chunk in enumerate(chunks, start=1):
            response = await model.ainvoke(
                [
                    ("system", summary.PARTIAL_PROMPT),
                    ("human", f"Trecho {index} de {len(chunks)}:\n\n{chunk}"),
                ]
            )
            partials.append(f"Trecho {index}:\n{response_text(response)}")

        response = await model.ainvoke(
            [
                ("system", summary.FINAL_PROMPT),
                ("human", "\n\n".join(partials)),
            ]
        )
        return {"summary_markdown": response_text(response)}

    return summarize

