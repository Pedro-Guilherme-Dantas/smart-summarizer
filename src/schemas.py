"""Contrato de texto normalizado, independente da origem da entrada."""

from pydantic import BaseModel, Field, field_validator


MAX_UPLOAD_BYTES = 256 * 1024
MAX_TEXT_CHARS = 120_000


class SourceDocument(BaseModel):
    source_label: str
    text: str = Field(max_length=MAX_TEXT_CHARS)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O arquivo de texto está vazio")
        return value


class ErrorResponse(BaseModel):
    detail: str


class LanguageDecision(BaseModel):
    detected_language: str
    needs_translation: bool
