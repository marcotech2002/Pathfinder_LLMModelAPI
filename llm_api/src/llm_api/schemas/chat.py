from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Definition of LLM model chat request
    """
    message: str


class ChatResponse(BaseModel):
    """
    Definition of LLM model chat response
    """
    response: str
