import json
from typing import Any
from config import config

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from assistant.models import DetermineDocumentStore, Answer, ContextDocument
from langchain_community.tools import DuckDuckGoSearchResults

EMBEDDINGS = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
VECTOR_STORE = FAISS.load_local(
    config.VECTOR_STORE_PATH, EMBEDDINGS, allow_dangerous_deserialization=True
)


def determine_document_search_chain(query: str, chat_history: list[str]) -> DetermineDocumentStore:
    
    with open("./prompts/determine_document_search.txt", "r") as file:
        template = file.read()
    
    prompt = PromptTemplate(input_variables=["response_format_model", "query", "chat_history"], template=template)
    chain = build_chain(prompt)

    parser = PydanticOutputParser(pydantic_object=DetermineDocumentStore)
    response = chain.invoke({
        "query": query, 
        "chat_history": chat_history, 
        "response_format_model": parser.get_format_instructions()
    }).content

    response_dict = json.loads(response)

    return DetermineDocumentStore(**response_dict)


def rag_documents(query: str) -> list[ContextDocument]:

    retrieved_docs = VECTOR_STORE.similarity_search(query)

    documents = convert_rag_documents(retrieved_docs)

    return documents

def convert_rag_documents(retrieved_docs: dict[str, Any]) -> list[ContextDocument]:

    documents = []

    for rag_doc in retrieved_docs:

        content = rag_doc.page_content
        link = rag_doc.metadata["source"]
        title = link.split("/")[-2]
        source = "rag"

        doc = ContextDocument(
            content=content,
            link=link,
            title=title,
            source=source,
        )

        documents.append(doc)

    return documents

def web_documents(query: str) -> list[ContextDocument]:

    search_tool = DuckDuckGoSearchResults(output_format="json")

    results = search_tool.invoke(query)
    results_json = json.loads(results)

    documents = convert_web_documents(results_json)

    return documents

def convert_web_documents(retrieved_docs: dict[str, Any])-> list[ContextDocument]:
    
    documents = []

    for web_doc in retrieved_docs:

        content = web_doc["snippet"]
        link = web_doc["link"]
        title = web_doc["title"]
        source = "web"

        doc = ContextDocument(
            content=content,
            link=link,
            title=title,
            source=source,
        )

        documents.append(doc)

    return documents


def answer_question_chain(
    query: str, 
    chat_history: list[str], 
    document_store_needed: bool, 
    context_documents: list[ContextDocument]
) -> Answer:

    with open("./prompts/answer_question.txt", "r") as file:
        template = file.read()
    
    prompt = PromptTemplate(input_variables=["response_format_model", "query", "chat_history", "documents_source", "context_documents"], template=template)
    chain = build_chain(prompt)

    parser = PydanticOutputParser(pydantic_object=Answer)

    source_field = generate_document_source_field(document_store_needed)
    response = chain.invoke({
        "query": query, 
        "chat_history": chat_history,
        "documents_source": source_field,
        "context_documents":context_documents, 
        "response_format_model": parser.get_format_instructions()
    }).content

    response_dict = json.loads(response)

    return Answer(**response_dict)


def generate_document_source_field(document_store_needed: bool) -> str:

    if document_store_needed:
        return "DuploCloud Document Store"
    else:
        return "Web Search"


def build_chain(prompt: str):

    model_kwargs = {"response_format": {"type": "json_object"}} 
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        max_tokens=None,
        timeout=config.LLM_TIMEOUT,
        max_retries=config.LLM_MAX_RETRIES,
        model_kwargs=model_kwargs,
    )

    chain = prompt | llm

    return chain