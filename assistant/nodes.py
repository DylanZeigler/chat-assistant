from assistant.models import GraphState
from assistant.llm import determine_document_search_chain, rag_chain, web_chain

def determine_document_search(state: GraphState):
    print("NODE: determine_document_search")
    query = state["query"]
    response = determine_document_search_chain(query)

    state["document_store_needed"] = response.document_store_needed

    return state

def llm_rag(state: GraphState):
    print("NODE: llm_rag")
    query = state["query"]
    response = rag_chain(query)

    # state["rag_documents"] = response["rag_documents"]
    # state["response"] = response["answer"]

    return state

def llm_web(state: GraphState):
    print("NODE: llm_web")
    query = state["query"]

    response = web_chain(query)
    # state["web_sources"] = response["web_sources"]
    # state["response"] = response["answer"]

    return state
