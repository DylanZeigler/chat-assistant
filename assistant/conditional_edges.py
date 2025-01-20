import logging
from assistant.models import GraphState

logger = logging.getLogger(__name__)

def route_document_search(
    state: GraphState,
)-> str:
    logger.info("CONDITIONAL EDGE: route_document_search")
    
    if state.document_store_needed:
        return "get_documents_rag"
    else:
        return "get_documents_web"
