from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class ContextDocument(BaseModel):
    content: str 
    link: str
    title: str
    source: str


class GraphState(TypedDict):
    context_documents: list[ContextDocument]
    response: str
    chat_history: list[str]
    query: str
    sources: list[str]
    document_store_needed: bool
    intro_message: str


class DetermineDocumentStore(BaseModel):
    document_store_needed: bool = Field(description=(
        "Field to determine whether the user is asking a question related to DuploCloud and a document store containing relevant "
        "DuploCloud information is needed to answer the users question. If the question is not related to DuploCloud then set this "
        "to False."
        )
    )

class Answer(BaseModel):
    chat_response: str = Field(description=(
        "Response you will give to answer the question from the user. This response should use the provided context documents to "
        "provide an accurate answer."
        )
    )
    intro_message: str = Field(description=(
        "Short phrase indicating which context source was used to provide the response. Sources are either 'DuploCloud documents' "
        "or 'Web search'"
        ),
        examples=[
            "Here is what I found from the DuploCloud Documents", 
            "Here is what I found from the web",
            "From the DuploCloud Documents", 
            "Searching the web says"
        ]
    )

