import time

from ..core.exceptions import GPUStatusError, ModelNotReadyError


class HealthCheckService:
    def __init__(self, llm_service, start_time):
        self.llm_service = llm_service
        self.start_time = start_time

    async def get_status(self):
        status = {
            "status": "ok",
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "model_ready": self.llm_service.is_model_loaded(),
            "model_name": getattr(self.llm_service, "model_name", None),
            "device": getattr(self.llm_service, "device", "unknown")
        }

        try:
            # agora retorna dict normal, não coroutine
            status["gpu"] = self._get_gpu_status()
        except GPUStatusError:
            status["gpu"] = None

        if not status["model_ready"]:
            raise ModelNotReadyError(status["model_name"])

        return status

    def _get_gpu_status(self):
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            return {
                "name": pynvml.nvmlDeviceGetName(handle).decode(),
                "memory_total_MB": round(mem.total / 1024**2, 2),
                "memory_used_MB": round(mem.used / 1024**2, 2),
                "memory_free_MB": round(mem.free / 1024**2, 2),
            }
        except Exception as e:
            raise GPUStatusError(str(e))
