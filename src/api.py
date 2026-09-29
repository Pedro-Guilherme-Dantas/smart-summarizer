"""Rotas HTTP para as diferentes origens de conteúdo."""

import logging
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

from .application import ModelProcessingError, PdfGenerationError, create_summary_pdf
from .inputs.errors import SourceInputError
from .inputs.txt import extract_txt
from .schemas import ErrorResponse


logger = logging.getLogger(__name__)
app = FastAPI(title="Smart Summarizer")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/v1/summaries/file",
    response_class=Response,
    responses={
        413: {"model": ErrorResponse},
        415: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
async def summarize_file(file: Annotated[UploadFile, File()]) -> Response:
    try:
        source = await extract_txt(file)
    except SourceInputError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    finally:
        await file.close()

    try:
        pdf = await create_summary_pdf(source)
    except ValueError as exc:
        logger.exception("Configuração do Gemini ausente ou inválida")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ModelProcessingError as exc:
        logger.exception("Falha no processamento do modelo")
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except PdfGenerationError as exc:
        logger.exception("Falha na renderização do PDF")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="resumo.pdf"'},
    )

