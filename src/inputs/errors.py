"""Erro de validação das origens de conteúdo."""


class SourceInputError(ValueError):
    def __init__(self, message: str, status_code: int = 422) -> None:
        super().__init__(message)
        self.status_code = status_code
