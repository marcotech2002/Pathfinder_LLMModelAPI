from typing import Optional
from pydantic import BaseModel


class GPUStatusResponse(BaseModel):
    """
    Definition of GPU status response
    """
    name: str
    memory_total_MB: float
    memory_used_MB: float
    memory_free_MB: float


class HealthCheckResponse(BaseModel):
    """
    Definition of health check response
    """
    status: str
    uptime_seconds: float
    model_ready: bool
    model_name: Optional[str] = None
    device: str
    gpu: Optional[GPUStatusResponse] = None
