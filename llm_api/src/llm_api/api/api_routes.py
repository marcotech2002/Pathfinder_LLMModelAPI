from fastapi import APIRouter, Depends

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
    Main endpoint for model communication.
    Exceptions are handled by global exception handlers.
    """
    response_text = await llm_service.generate_response(request.mensagem)
    return ChatResponse(resposta=response_text)
