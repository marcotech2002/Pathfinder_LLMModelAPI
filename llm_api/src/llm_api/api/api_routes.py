from fastapi import APIRouter, HTTPException, Depends

from ..schemas.chat import ChatRequest, ChatResponse
from ..services.llm_service import LLMService

router = APIRouter()


def get_llm_service() -> LLMService:
    """Dependency injection"""
    from ..main import llm_service
    return llm_service


@router.post("/chat", response_model=ChatResponse, status_code=200)
async def chat_endpoint(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
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
