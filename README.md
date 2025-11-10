# Instruções para carregar o projeto com Poetry

1. **Pré-requisitos**
    - Tenha o [Poetry](https://python-poetry.org/docs/#installation) instalado em seu sistema.
    - Certifique-se de ter o Python na versão compatível definida em `pyproject.toml`.

2. **Clone o repositório**
    ```bash
    git clone https://github.com/marcotech2002/Pathfinder_LLMModelAPI.git
    cd Pathfinder_LLMModelAPI/llm_api
    ```

3. **Instale as dependências**
    ```bash
    poetry install
    ```

4. **Ative o ambiente virtual do Poetry**
    ```bash
    poetry shell
    ```

5. **Execute o projeto conforme instruções específicas**
    ```bash
    poetry run uvicorn src.llm_api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
