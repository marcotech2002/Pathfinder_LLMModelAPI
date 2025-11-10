from prometheus_client import Counter, Histogram, Gauge
import psutil
import pynvml

REQUEST_COUNT = Counter(
    "llm_requests_total",
    "Número total de requisições ao modelo LLM"
)

REQUEST_LATENCY = Histogram(
    "llm_request_latency_seconds",
    "Tempo de resposta do modelo LLM"
)

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "Uso de CPU em porcentagem"
)

GPU_USAGE = Gauge(
    "gpu_usage_percent",
    "Uso de GPU em porcentagem (se disponível)"
)


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        GPU_USAGE.set(util.gpu)
    except Exception:
        pass
