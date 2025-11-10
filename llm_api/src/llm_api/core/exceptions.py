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
            f"O modelo '{model_name}' não foi encontrado.")


class LLMModelNotLoadedError(LLMServiceError):
    """
    Exception raised when attempting to use the model before it is loaded.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(
            f"O modelo '{model_name}' não está carregado ou pronto para uso.")


class OllamaConnectionError(LLMServiceError):
    """
    Exception raised when the API fails to communicate
    with the Ollama server.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        super().__init__(
            (
                f"Falha ao conectar ao serviço Ollama na URL: {base_url}. "
                "Verifique se o servidor está ativo."
            )
        )


class ModelGenerationError(LLMServiceError):
    """
    Exception raised when response generation fails after connection.
    """

    def __init__(self, details: str):
        self.details = details
        super().__init__(
            f"Erro durante a geração da resposta pelo modelo LLM. {details}")


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
