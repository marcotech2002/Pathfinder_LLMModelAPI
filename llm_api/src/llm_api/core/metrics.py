from prometheus_client import Counter, Histogram, Gauge
import psutil
import pynvml

REQUEST_COUNT = Counter(
    "llm_requests_total",
    "Total number of requests to the LLM model API"
)

REQUEST_LATENCY = Histogram(
    "llm_request_latency_seconds",
    "Response time of the LLM model"
)

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "CPU usage percentage"
)

GPU_USAGE = Gauge(
    "gpu_usage_percent",
    "GPU usage percentage (if available)"
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
