# API para utilização de modelo LLM local

Este projeto fornece uma API REST para interação com modelos de linguagem executados localmente, utilizando o servidor **Ollama** como backend.  
A API é construída com **FastAPI** e estruturada seguindo boas práticas de organização em camadas (services, schemas, core, etc.), incluindo:

### Tecnologias Utilizadas
- **Python 3.12+**
- **FastAPI** para exposição da API
- **Poetry** para gerenciamento de dependências
- **Uvicorn** como servidor ASGI
- **Ollama** para execução de modelos LLM localmente
- **Prometheus Client** para métricas /monitoring
- **psutil** para leitura de uso de CPU
- **pynvml** (opcional) para leitura de uso de GPU NVIDIA

A API oferece:
- Endpoint de chat para interação com o modelo (`api/chat`)
- Health Check completo com status do modelo e GPU (`api/status`)
- Métricas para monitoramento (`api/metrics`)

Documentação Swagger (`/docs`)

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
    
# Instruções para utilização de modelos do Ollama

1. **Instalar o Ollama**: https://ollama.com

2. **Instalar modelo a sua escolha (o modelo utilizado foi o llama3)**
    ```bash
    ollama pull llama3
    ```

# Rodar a aplicação via terminal
```bash
poetry run uvicorn src.llm_api.main:app --host 0.0.0.0 --port 8000 --reload
```
