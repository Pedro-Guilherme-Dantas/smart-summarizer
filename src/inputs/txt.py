"""Leitura da entrada TXT enviada pela API."""

from pathlib import PurePath

from fastapi import UploadFile
from pydantic import ValidationError

from .errors import SourceInputError
from ..schemas import MAX_UPLOAD_BYTES, SourceDocument


async def extract_txt(file: UploadFile) -> SourceDocument:
    filename = PurePath(file.filename or "").name
    if not filename.lower().endswith(".txt"):
        raise SourceInputError("Envie um arquivo .txt em UTF-8", status_code=415)

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise SourceInputError("O arquivo excede o limite de 256 KiB", status_code=413)

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SourceInputError("O arquivo deve estar codificado em UTF-8") from exc

    if "\x00" in text:
        raise SourceInputError("O arquivo contém dados binários")

    try:
        return SourceDocument(
            source_label=filename,
            text=text.replace("\r\n", "\n").replace("\r", "\n"),
        )
    except ValidationError as exc:
        if not text.strip():
            raise SourceInputError("O arquivo de texto está vazio") from exc
        raise SourceInputError("O texto excede o limite de 120.000 caracteres") from exc
