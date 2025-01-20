from typing import Optional
from pydantic import BaseModel, Field

class ContextDocument(BaseModel):
    content: str = Field(description="Text of document.")
    link: str = Field(description="Link to document.")
    title: str = Field(description="Title of the document")
    source: str = Field(description="Whether the document is from RAG or Web.")


class GraphState(BaseModel):
    context_documents: Optional[list[ContextDocument]] = Field([], description="Context Documents from either RAG or the Web.")
    response: Optional[str] = Field("", description="Chtbot Response to the query.")
    chat_history: Optional[list[str]] = Field([], description="History of the chat from the user.")
    query: str = Field(description="Message to respond to.")
    document_store_needed: Optional[bool | None] = Field(None, description="Whether to run RAG or not.")
    intro_message: Optional[str] = Field("", description="Message to indicate where answer is sourced from.")


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

