from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..services.llm_service import LLMService
from ..services.health_check_service import HealthCheckService
from ..schemas.health_check import HealthCheckResponse


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


@router.get("/status", response_model=HealthCheckResponse)
def health_check(service: HealthCheckService = Depends(get_health_service)):
    status = service.get_status()

    if status["status"] != "ok":
        return JSONResponse(status_code=503, content=status)

    return status
