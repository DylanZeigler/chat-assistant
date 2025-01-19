

from langgraph.graph import StateGraph, START, END

from assistant.nodes import determine_document_search, llm_rag, llm_web
from assistant.conditional_edges import route_document_search
from assistant.models import GraphState

GRAPH = StateGraph(GraphState)

GRAPH.add_node("determine_document_search", determine_document_search)
GRAPH.add_node("llm_rag", llm_rag)
GRAPH.add_node("llm_web", llm_web)

GRAPH.add_conditional_edges(
    "determine_document_search",
    route_document_search,
    {"llm_rag": "llm_rag", "llm_web": "llm_web"},
)

GRAPH.add_edge(START, "determine_document_search")
GRAPH.add_edge("llm_rag", END)
GRAPH.add_edge("llm_web", END)

COMPILED_GRAPH = GRAPH.compile()


def run_graph(query):
    input_state = {"query": query}
    response = COMPILED_GRAPH.invoke(input_state)

    return response
