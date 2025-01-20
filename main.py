from dotenv import load_dotenv
load_dotenv()

from config import config
from fastapi import FastAPI
import logging 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

from data.load_vectors import load_data
load_data()

from api.endpoints import router

def create_app():
    app = FastAPI(
        title=config.API_TITLE,
        version=config.API_VERSION,
        description=config.API_DESCRIPTION,
        openapi_url="/openapi.json",
        docs_url="/",
    )

    app.include_router(router)

    return app

app = create_app()
