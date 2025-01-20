import logging

from assistant.models import GraphState
from assistant.llm_utils import determine_document_search_chain, rag_documents, web_documents, answer_question_chain

logger = logging.getLogger(__name__)

def determine_document_search(state: GraphState):
    logger.info("NODE: determine_document_search")
    query = state["query"]
    response = determine_document_search_chain(query)

    state["document_store_needed"] = response.document_store_needed

    return state


def get_documents_rag(state: GraphState):
    logger.info("NODE: get_documents_rag")
    query = state["query"]
    response = rag_documents(query)

    state["context_documents"] = response

    return state

def get_documents_web(state: GraphState):
    logger.info("NODE: get_documents_web")
    query = state["query"]

    response = web_documents(query)
    state["context_documents"] = response

    return state


def answer_question(state: GraphState):
    logger.info("NODE: answer_question")
    query = state["query"]
    context_documents = state["context_documents"]
    document_store_needed = state["document_store_needed"]

    response = answer_question_chain(query, document_store_needed, context_documents)
    state["response"] = response.chat_response
    state["intro_message"] = response.intro_message

    return state

