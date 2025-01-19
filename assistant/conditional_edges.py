from assistant.models import GraphState

def route_document_search(
    state: GraphState,
):
    print("CONDITIONAL EDGE: route_document_search")
    
    if state["document_store_needed"]:
        return "llm_rag"
    else:
        return "llm_web"
