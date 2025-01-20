from typing import Optional
from pydantic import BaseModel, Field
from assistant.models import ContextDocument


class ChatRequest(BaseModel):
    query: str = Field(description="Message to be directly responded to by the chatbot.")
    chat_history: Optional[list[str]] = Field(description="Previous chat history used for context.")

class ChatResponse(BaseModel):
    intro_message: str = Field(description="Chatbot message to indicate where the response originated from.")
    response: str = Field(description="Chatbot response to the query.")
    context_documents: list[ContextDocument] = Field(description="Documents used by the chatbot to assist in answering the user.")
    original_query: str = Field(description="Message responded to by the chatbot.")