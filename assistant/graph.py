

from langgraph.graph import StateGraph, START, END

from assistant.nodes import determine_document_search, get_documents_rag, get_documents_web, answer_question
from assistant.conditional_edges import route_document_search
from assistant.models import GraphState

GRAPH = StateGraph(GraphState)

GRAPH.add_node("determine_document_search", determine_document_search)
GRAPH.add_node("get_documents_rag", get_documents_rag)
GRAPH.add_node("get_documents_web", get_documents_web)
GRAPH.add_node("answer_question", answer_question)

GRAPH.add_conditional_edges(
    "determine_document_search",
    route_document_search,
    {"get_documents_rag": "get_documents_rag", "get_documents_web": "get_documents_web"},
)

GRAPH.add_edge(START, "determine_document_search")
GRAPH.add_edge("get_documents_rag", "answer_question")
GRAPH.add_edge("get_documents_web", "answer_question")
GRAPH.add_edge("answer_question", END)

COMPILED_GRAPH = GRAPH.compile()

COMPILED_GRAPH.get_graph().draw_mermaid_png(output_file_path="./assistant/graph.png")

def run_graph(query):
    input_state = {"query": query}
    response = COMPILED_GRAPH.invoke(input_state)

    return response
