import logging
from fastapi import APIRouter
from assistant.graph import run_graph
from api.models import ChatRequest, ChatResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/chat", 
    response_model=ChatResponse, 
    status_code=201, 
    summary="Chat Completion", 
    description="AI assistant that responses to chat queries"
)
def create_item(request: ChatRequest):

    logger.info(f"Chat endpoint called with request: {request}")

    result = run_graph(query=request.query, chat_history=request.chat_history)
    response = ChatResponse(
        intro_message=result["intro_message"], 
        response=result["response"], 
        context_documents=result["context_documents"], 
        original_query=result["query"]
    )

    return response

@router.get("/health", summary="Health Check", description="Check status of the API")
def create_item():
    return 