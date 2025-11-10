import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .api.api_routes import router as chat_router
from .services.llm_service import LLMService
from .core.config import settings


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


llm_service = LLMService(model_name=settings.LLM_MODEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan function
    """
    logger.info(
        (
            f"Iniciando a API. Tentando carregar o modelo LLM: "
            f"{settings.LLM_MODEL}"
        )
    )

    try:
        await llm_service.initialize_model()
        logger.info(
            (
                f"Modelo {settings.LLM_MODEL} "
                "carregado com sucesso e pronto para uso."
            )
        )
    except Exception as e:
        logger.error(f"Erro fatal ao inicializar o modelo LLM: {e}")
    yield

    logger.info("Encerrando a API.")


app = FastAPI(
    title="API para comunicação com modelo LLM local",
    description=(
        "Sistema para utilização do modelo llama3 "
        "via requisições HTTP"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(chat_router, prefix="/api")


@app.get("/status")
def health_check():
    """Endpoint to check if the server is active"""
    return {"status": "ok", "model_ready": llm_service.is_model_loaded()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
