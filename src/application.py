"""Executa o fluxo comum a todas as origens de texto."""

from fastapi.concurrency import run_in_threadpool

from .config import create_gemini_model
from .graph import build_graph
from .schemas import SourceDocument
from .services.pdf_renderer import render_pdf


class ModelProcessingError(RuntimeError):
    pass


class PdfGenerationError(RuntimeError):
    pass


async def create_summary_pdf(source: SourceDocument) -> bytes:
    model = create_gemini_model()
    try:
        result = await build_graph(model).ainvoke(
            {"source_text": source.text, "source_label": source.source_label}
        )
    except Exception as exc:
        raise ModelProcessingError("Falha ao processar o texto com o modelo") from exc

    try:
        return await run_in_threadpool(render_pdf, result["document_markdown"])
    except Exception as exc:
        raise PdfGenerationError("Falha ao gerar o PDF") from exc
