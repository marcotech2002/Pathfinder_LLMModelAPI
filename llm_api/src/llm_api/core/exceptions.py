from fastapi import HTTPException
from starlette import status


class LLMServiceError(Exception):
    """
    Exception for errors in the LLM service layer.
    """
    pass


class LLMModelNotFoundError(LLMServiceError):
    """
    Exception raised when the model was not found.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(
            f"Model '{model_name}' was not found.")


class LLMModelNotLoadedError(LLMServiceError):
    """
    Exception raised when attempting to use the model before it is loaded.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(
            f"Model '{model_name}' is not loaded or ready for use.")


class OllamaConnectionError(LLMServiceError):
    """
    Exception raised when the API fails to communicate
    with the Ollama server.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        super().__init__(
            (
                f"Failed to connect to Ollama service at URL: {base_url}. "
                "Please check if the server is running."
            )
        )


class ModelGenerationError(LLMServiceError):
    """
    Exception raised when response generation fails after connection.
    """

    def __init__(self, details: str):
        self.details = details
        super().__init__(
            f"Error during LLM model response generation. {details}")


class ServiceUnavailableHTTPException(HTTPException):
    """
    Exception raised when the service is unavailable.
    """

    def __init__(
        self,
        detail: str = "The LLM model is offline or not ready.",
        headers: dict | None = None
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            headers=headers
        )


class HealthCheckServiceError(Exception):
    """
    Base exception for errors in the Health Check service.
    """
    pass


class ModelNotReadyError(HealthCheckServiceError):
    """
    Exception raised when the model is not loaded and ready.
    """

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name
        msg = (
            f"Model '{model_name}' is not ready or not loaded."
            if model_name else
            "The model is not ready or not loaded."
        )
        super().__init__(msg)


class GPUStatusError(HealthCheckServiceError):
    """
    Exception raised when GPU status cannot be retrieved.
    """

    def __init__(self, details: str | None = None):
        msg = (
            f"Unable to retrieve GPU status. {details}"
            if details else
            "Unable to retrieve GPU status."
        )
        super().__init__(msg)
