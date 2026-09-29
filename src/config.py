import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def create_gemini_model() -> ChatGoogleGenerativeAI:
    """Carrega a configuração e cria o cliente Gemini para o grafo."""
    load_dotenv(dotenv_path=_ENV_FILE, override=False)

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "").strip()

    missing = [
        name
        for name, value in (("GOOGLE_API_KEY", api_key), ("GEMINI_MODEL", model_name))
        if not value
    ]
    if missing:
        raise ValueError(f"Defina {', '.join(missing)} no ambiente ou no arquivo .env")

    return ChatGoogleGenerativeAI(model=model_name, api_key=api_key)

