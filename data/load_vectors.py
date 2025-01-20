import os
import logging
import requests

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config import config

logger = logging.getLogger(__name__)

def fetch_file_urls(repo_owner, repo_name, directory_path):
    """
    Fetch all files in a specific directory of a GitHub repository.

    :param repo_owner: Owner of the repository (e.g., 'octocat').
    :param repo_name: Name of the repository (e.g., 'Hello-World').
    :param directory_path: Path to the target directory within the repository.
    :return: List of file paths within the specified directory.
    """
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}"
    headers = {}

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        files = []
        contents = response.json()

        for item in contents:
            if item['type'] == 'file':
                files.append(item['download_url'])
        return files
    else:
        raise Exception(f"Failed to fetch files: {response.status_code} - {response.text}")


def load_documents(file_urls):

    loader = WebBaseLoader(file_urls)
    documents = loader.load()

    return documents


def split_documents(documents):

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    
    return texts


def run_embeddings_and_create_vector_store(texts):

    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(texts, embeddings)

    return vector_store


def save_vector_store_locally(vector_store):

    if not os.path.exists(config.VECTOR_STORE_DIR):
        os.makedirs(config.VECTOR_STORE_DIR)

    vector_store.save_local(config.VECTOR_STORE_PATH)


def check_vector_store_exists():

    return os.path.isdir(config.VECTOR_STORE_PATH)


def load_data():

    if check_vector_store_exists():
        logger.info("Data already loaded")
        return 
    
    logger.info("Data does not exist, loading data now...")
    
    file_urls = fetch_file_urls(repo_owner=config.REPO_OWNER, repo_name=config.REPO_NAME, directory_path=config.DIRECTORY_PATH)
    documents = load_documents(file_urls=file_urls)
    texts = split_documents(documents=documents)
    vector_store = run_embeddings_and_create_vector_store(texts=texts)
    save_vector_store_locally(vector_store=vector_store)


if __name__ == "__main__":
    load_data()