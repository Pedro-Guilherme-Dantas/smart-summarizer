"""Divisão de texto em trechos para chamadas controladas ao modelo."""

MAX_CHUNK_CHARS = 6_000
LANGUAGE_SAMPLE_CHARS = 12_000


def split_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    if max_chars < 1:
        raise ValueError("max_chars deve ser positivo")

    remaining = text.strip()
    chunks: list[str] = []
    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining)
            break

        cut = max_chars
        for index in range(max_chars, max_chars // 2, -1):
            if remaining[index - 1].isspace():
                cut = index
                break

        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].lstrip()

    return chunks


def sample_for_language(text: str) -> str:
    """Amostra início, meio e fim para limitar o custo da classificação."""
    if len(text) <= LANGUAGE_SAMPLE_CHARS:
        return text

    part_size = LANGUAGE_SAMPLE_CHARS // 3
    middle = (len(text) - part_size) // 2
    return (
        f"[Início]\n{text[:part_size]}\n\n"
        f"[Meio]\n{text[middle:middle + part_size]}\n\n"
        f"[Fim]\n{text[-part_size:]}"
    )

