import logging
from fastapi import APIRouter
from assistant.graph import run_graph

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat", summary="Chat Completion", description="AI assistant that responses to chat queries")
def create_item(query: str):

    logger.info(f"Chat endpoint called with query: {query}")

    result = run_graph(query)
    return result

@router.get("/health", summary="Health Check", description="Check status of the API")
def create_item():
    return 