from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    """

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    LOG_LEVEL: str = "INFO"

    LLM_MODEL: str = "llama3"

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    CACHE_TYPE: str = "memory"

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
