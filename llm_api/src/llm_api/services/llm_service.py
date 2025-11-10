import ollama


class LLMService:
    def __init__(self, model_name: str):
        """Model service initialization"""
        self.model_name = model_name
        self._is_loaded = False
        self.client = ollama.AsyncClient()

    def is_model_loaded(self) -> bool:
        """Model loading status"""
        return self._is_loaded

    async def initialize_model(self):
        """Ollama model initialization"""
        try:
            await self.client.list()
            self._is_loaded = True
        except Exception as e:
            raise ConnectionError(
                (
                    "Ollama Service não está acessível ou modelo "
                    f"{self.model_name} não está pronto. Erro: {e}"
                )
            )

    async def generate_response(self, message: str) -> str:
        """Model usage"""
        response = await self.client.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': message}],
            stream=False
        )
        return response['message']['content']
