import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import time

from .api.api_routes import router as chat_router
from .api.exception_handlers import (
    gpu_status_error_handler,
    health_check_service_error_handler,
    llm_model_not_found_handler,
    llm_model_not_loaded_handler,
    model_not_ready_handler,
    ollama_connection_error_handler,
    model_generation_error_handler,
    generic_llm_service_error_handler
)
from .core.exceptions import (
    GPUStatusError,
    HealthCheckServiceError,
    LLMServiceError,
    LLMModelNotFoundError,
    LLMModelNotLoadedError,
    ModelNotReadyError,
    OllamaConnectionError,
    ModelGenerationError
)
from .services.llm_service import LLMService
from .core.config import settings


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

START_TIME = time.time()

llm_service = LLMService(model_name=settings.LLM_MODEL,
                         base_url=settings.OLLAMA_BASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan context manager.
    """
    logger.info(f"Starting API. Loading model: {settings.LLM_MODEL}")
    try:
        await llm_service.initialize_model()
        logger.info(f"Model {settings.LLM_MODEL} loaded successfully.")
    except Exception as e:
        logger.error(f"{e}")
    yield
    logger.info("Closing application.")


app = FastAPI(
    title="LLM Model API usage",
    description=(
        f"System for using the {settings.LLM_MODEL} model "
        "via HTTP requests through Ollama."
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
app.add_exception_handler(ModelNotReadyError, model_not_ready_handler)
app.add_exception_handler(GPUStatusError, gpu_status_error_handler)
app.add_exception_handler(HealthCheckServiceError,
                          health_check_service_error_handler)


app.include_router(chat_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
