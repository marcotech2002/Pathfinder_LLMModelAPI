from ollama import AsyncClient, RequestError
import httpx
import logging

from ..core.exceptions import (
    LLMModelNotFoundError,
    OllamaConnectionError,
    ModelGenerationError,
    LLMModelNotLoadedError
)

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, model_name: str, base_url: str):
        """Model service initialization"""
        self.model_name = model_name
        self.base_url = base_url
        self._is_loaded = False
        self.client = AsyncClient(host=self.base_url)

    def is_model_loaded(self) -> bool:
        """Model loading status"""
        return self._is_loaded

    async def initialize_model(self):
        """Ollama model initialization"""
        try:
            response = await self.client.list()
            logger.debug(f"Resposta completa de list(): {response}")
            logger.debug(f"Tipo da resposta: {type(response)}")

            models_list = []
            if isinstance(response, dict):
                models_list = response.get('models', [])
            elif hasattr(response, 'models'):
                models_list = response.models
            else:
                models_list = response if isinstance(response, list) else []

            logger.debug(f"Lista de modelos extraída: {models_list}")

            model_names = []
            for model in models_list:
                logger.debug(
                    f"Processando modelo: {model} (tipo: {type(model)})")

                model_name = None

                if isinstance(model, dict):
                    model_name = (
                        model.get('name') or
                        model.get('model') or
                        model.get('digest')
                    )
                elif isinstance(model, str):
                    model_name = model
                else:
                    model_name = (
                        getattr(model, 'name', None) or
                        getattr(model, 'model', None)
                    )

                if model_name:
                    base_name = model_name.split(':')[0]
                    model_names.append(model_name)
                    if base_name != model_name:
                        model_names.append(base_name)

            logger.info(f"Modelos disponíveis: {model_names}")

            if model_names and self.model_name not in model_names:
                if f"{self.model_name}:latest" not in model_names:
                    raise LLMModelNotFoundError(self.model_name)

            self._is_loaded = True
            logger.info(f"Modelo {self.model_name} inicializado com sucesso")

        except RequestError as e:
            logger.error(f"RequestError ao conectar: {e}")
            raise OllamaConnectionError(self.base_url) from e
        except httpx.ConnectError as e:
            logger.error(f"ConnectError ao conectar: {e}")
            raise OllamaConnectionError(self.base_url) from e
        except (LLMModelNotFoundError, OllamaConnectionError):
            raise
        except Exception as e:
            logger.error(
                f"Erro inesperado na inicialização: {e}", exc_info=True)
            raise ModelGenerationError(
                f"Houve falha na inicialização do cliente: {e}") from e

    async def generate_response(self, prompt: str) -> str:
        """
        Generate response from the model
        """
        if not self._is_loaded:
            raise LLMModelNotLoadedError(self.model_name)

        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )

            logger.debug(f"Resposta do chat: {response}")
            logger.debug(f"Tipo da resposta do chat: {type(response)}")

            if isinstance(response, dict):
                content = response.get('message', {}).get('content')
                if content:
                    return content
            elif hasattr(response, 'message'):
                if hasattr(response.message, 'content'):
                    return response.message.content
                elif isinstance(response.message, dict):
                    return response.message.get('content', '')

            logger.error(f"Estrutura da resposta: {dir(response)}")
            raise ModelGenerationError(
                f"Formato de resposta não reconhecido: {type(response)}")

        except RequestError as e:
            logger.error(f"RequestError durante geração: {e}")
            raise ModelGenerationError(str(e)) from e
        except (KeyError, AttributeError) as e:
            logger.error(f"Erro de acesso aos dados da resposta: {e}")
            raise ModelGenerationError(
                f"Formato de resposta inesperado: {e}") from e
        except ModelGenerationError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            raise ModelGenerationError(f"Erro inesperado: {e}") from e
