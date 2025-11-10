import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .api.api_routes import router as chat_router
from .api.exception_handlers import (
    llm_model_not_found_handler,
    llm_model_not_loaded_handler,
    ollama_connection_error_handler,
    model_generation_error_handler,
    generic_llm_service_error_handler
)
from .core.exceptions import (
    LLMServiceError,
    LLMModelNotFoundError,
    LLMModelNotLoadedError,
    OllamaConnectionError,
    ModelGenerationError
)
from .services.llm_service import LLMService
from .core.config import settings


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


llm_service = LLMService(model_name=settings.LLM_MODEL,
                         base_url=settings.OLLAMA_BASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan context manager.
    """
    logger.info(f"Iniciando a API. Carregando modelo: {settings.LLM_MODEL}")
    try:
        await llm_service.initialize_model()
        logger.info(f"Modelo {settings.LLM_MODEL} carregado com sucesso.")
    except Exception as e:
        logger.error(f"{e}")
    yield
    logger.info("Encerrando a API.")


app = FastAPI(
    title="API para comunicação com modelo LLM local",
    description=(
        "Sistema para utilização do modelo llama3 via requisições HTTP"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

app.add_exception_handler(LLMModelNotFoundError, llm_model_not_found_handler)
app.add_exception_handler(LLMModelNotLoadedError, llm_model_not_loaded_handler)
app.add_exception_handler(OllamaConnectionError,
                          ollama_connection_error_handler)
app.add_exception_handler(ModelGenerationError, model_generation_error_handler)
app.add_exception_handler(LLMServiceError, generic_llm_service_error_handler)

app.include_router(chat_router, prefix="/api")


@app.get("/status")
def health_check():
    """
    Endpoint to check the service status and if the model is loaded.
    """
    return {"status": "ok", "model_ready": llm_service.is_model_loaded()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
