from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    
    # LLM
    OPENAI_API_KEY: str
    USER_AGENT: str
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.0
    LLM_TIMEOUT: int = 30
    LLM_MAX_RETRIES: int = 2
    EMBEDDING_MODEL: str = "text-embedding-3-large"

    # DOCUMENT GITHUB LOCATION
    REPO_OWNER: str = "duplocloud" 
    REPO_NAME: str = "docs"  
    DIRECTORY_PATH: str = "getting-started-1/application-focussed-interface"
    VECTOR_STORE_DIR: str =  "data/stores"
    VECTOR_STORE_NAME: str = "faiss_vector_store"
    VECTOR_STORE_PATH: str = VECTOR_STORE_DIR + "/" + VECTOR_STORE_NAME

    # API 
    API_TITLE: str = "Dylan Zeigler's Chat AI"
    API_VERSION: str = "v0.1.0"
    API_DESCRIPTION: str = (
        "API that exposes a chat completion endpoint to respond to users questions. The chat AI either uses a vector store or the web "
        "to answer the users questions."
    )

    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).parent}/.env",
        case_sensitive=True,
        extra="allow",
    )

config: AppConfig = AppConfig()