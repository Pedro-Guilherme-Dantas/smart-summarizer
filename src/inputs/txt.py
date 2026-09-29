"""Leitura da entrada TXT enviada pela API."""

from pathlib import PurePath

from fastapi import UploadFile

from ..schemas import MAX_UPLOAD_BYTES, SourceDocument


async def extract_txt(file: UploadFile) -> SourceDocument:
    filename = PurePath(file.filename or "").name
    if not filename.lower().endswith(".txt"):
        raise ValueError("Envie um arquivo .txt em UTF-8")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("O arquivo excede o limite de 256 KiB")

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("O arquivo deve estar codificado em UTF-8") from exc

    if "\x00" in text:
        raise ValueError("O arquivo contém dados binários")

    return SourceDocument(
        source_label=filename,
        text=text.replace("\r\n", "\n").replace("\r", "\n"),
    )
