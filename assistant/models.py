from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class GraphState(TypedDict):
    rag_documents: list[str]
    response: str
    chat_history: list[str]
    query: str
    web_sources: list[str]
    document_store_needed: bool


class DetermineDocumentStore(BaseModel):
    document_store_needed: bool = Field(description=(
        "Field to determine whether the user is asking a question related to DuploCloud and a document store containing relevant "
        "DuploCloud information is needed to answer the users question. If the question is not related to DuploCloud then set this "
        "to False."
        )
    )
