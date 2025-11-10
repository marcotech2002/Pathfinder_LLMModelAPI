from fastapi import Request, status
from fastapi.responses import JSONResponse

from ..core.exceptions import (
    GPUStatusError,
    HealthCheckServiceError,
    LLMServiceError,
    LLMModelNotFoundError,
    LLMModelNotLoadedError,
    ModelNotReadyError,
    OllamaConnectionError,
    ModelGenerationError
)


async def llm_model_not_found_handler(
    request: Request,
    exc: LLMModelNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "model_name": exc.model_name,
            "error_type": "model_not_found"
        }
    )


async def llm_model_not_loaded_handler(
    request: Request,
    exc: LLMModelNotLoadedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": str(exc),
            "model_name": exc.model_name,
            "error_type": "model_not_loaded"
        }
    )


async def ollama_connection_error_handler(
    request: Request,
    exc: OllamaConnectionError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "detail": str(exc),
            "base_url": exc.base_url,
            "error_type": "connection_error"
        }
    )


async def model_generation_error_handler(
    request: Request,
    exc: ModelGenerationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error_details": exc.details,
            "error_type": "generation_error"
        }
    )


async def generic_llm_service_error_handler(
    request: Request,
    exc: LLMServiceError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error_type": "llm_service_error"
        }
    )


async def model_not_ready_handler(
    request: Request, exc: ModelNotReadyError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": str(exc),
            "model_name": exc.model_name,
            "error_type": "model_not_ready"
        }
    )


async def gpu_status_error_handler(
    request: Request, exc: GPUStatusError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": str(exc),
            "gpu_status": "unavailable",
            "error_type": "gpu_status_error"
        }
    )


async def health_check_service_error_handler(
    request: Request, exc: HealthCheckServiceError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error_type": "health_check_service_error"
        }
    )
