"""Normaliza a saída textual do modelo para um documento Markdown."""


def prepare_markdown(summary: str) -> str:
    markdown = summary.strip()
    if markdown.startswith("```") and markdown.endswith("```"):
        markdown = "\n".join(markdown.splitlines()[1:-1]).strip()
    if not markdown:
        raise ValueError("O resumo está vazio")
    if not markdown.startswith("# "):
        markdown = f"# Resumo\n\n{markdown}"
    return markdown + "\n"

