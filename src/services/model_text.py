"""Extrai somente o texto de uma resposta do modelo."""

from langchain_core.messages import AIMessage


def response_text(response: AIMessage) -> str:
    content = response.content
    if isinstance(content, str):
        result = content.strip()
    else:
        result = "\n".join(
            block if isinstance(block, str) else block.get("text", "")
            for block in content
            if isinstance(block, str) or block.get("type") == "text"
        ).strip()

    if not result:
        raise RuntimeError("O modelo retornou uma resposta vazia")
    return result
