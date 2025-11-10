from fastapi import APIRouter, Depends, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from ..services.llm_service import LLMService
from ..services.health_check_service import HealthCheckService
from ..schemas.health_check import HealthCheckResponse
from ..schemas.chat import ChatRequest, ChatResponse


router = APIRouter()


def get_llm_service() -> LLMService:
    from ..main import llm_service
    return llm_service


def get_start_time() -> float:
    from ..main import START_TIME
    return START_TIME


def get_health_service(
        llm_service: LLMService = Depends(get_llm_service),
        start_time: float = Depends(get_start_time)
) -> HealthCheckService:
    return HealthCheckService(llm_service, start_time)


@router.post("/chat", response_model=ChatResponse, status_code=200)
async def model_chat(
    request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)
):
    """
    Main endpoint for model communication.
    """
    response_text = await llm_service.generate_response(request.message)
    return response_text


@router.get("/metrics")
def get_application_metrics():
    """
    Endpoint to expose application metrics for monitoring.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get("/status", response_model=HealthCheckResponse)
async def get_health_check(
    health_check_service: HealthCheckService = Depends(get_health_service)
):
    """
    Endpoint to check the health status of the application.
    """
    return await health_check_service.get_status()
