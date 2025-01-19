from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    
    REPO_OWNER: str = "duplocloud" 
    REPO_NAME: str = "docs"  
    DIRECTORY_PATH: str = "getting-started-1/application-focussed-interface"  
    VECTOR_STORE_PATH: str = "./data/stores/faiss_vector_store"

    LLM_TEMPERATURE: float = 0.0


config: AppConfig = AppConfig()