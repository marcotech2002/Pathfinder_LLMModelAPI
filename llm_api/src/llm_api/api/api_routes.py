from fastapi import APIRouter, HTTPException

from ..main import llm_service
from ..schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, status_code=200)
async def chat_endpoint(request: ChatRequest):
    """
    Main endpoint for model communication
    """
    if not llm_service.is_model_loaded():
        raise HTTPException(
            status_code=503, detail="Modelo LLM não está carregado ou pronto.")

    try:
        response_text = await llm_service.generate_response(request.mensagem)

        return ChatResponse(resposta=response_text)

    except ConnectionError:
        raise HTTPException(
            status_code=500, detail="Erro de comunicação com o serviço Ollama."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao gerar resposta: {e}")
