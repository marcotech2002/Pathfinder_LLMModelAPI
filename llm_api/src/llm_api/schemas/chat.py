from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Definition of LLM model chat request"""
    mensagem: str


class ChatResponse(BaseModel):
    """Definition of LLM model chat response"""
    resposta: str


class ChatHistoryItem(BaseModel):
    """Definition of LLM model chat history"""
    role: str
    content: str
