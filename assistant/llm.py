import json
from config import config

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from assistant.models import DetermineDocumentStore

EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-large")
VECTOR_STORE = FAISS.load_local(
    config.VECTOR_STORE_PATH, EMBEDDINGS, allow_dangerous_deserialization=True
)


def determine_document_search_chain(query):
    
    with open("./prompts/determine_document_search.txt", "r") as file:
        template = file.read()
    
    prompt = PromptTemplate(input_variables=["response_format_model", "chat_conversation"], template=template)

    model_kwargs = {"response_format": {"type": "json_object"}} 
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=config.LLM_TEMPERATURE,
        max_tokens=None,
        timeout=30,
        max_retries=2,
        model_kwargs=model_kwargs,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    parser = PydanticOutputParser(pydantic_object=DetermineDocumentStore)

    response = chain.run({"chat_conversation": query, "response_format_model": parser.get_format_instructions()})

    response_dict = json.loads(response)

    return DetermineDocumentStore(**response_dict)



def rag_chain(query):

    return {}

def web_chain(query):

    return {}