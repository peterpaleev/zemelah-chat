# flake8: noqa: E402
from dotenv import load_dotenv

load_dotenv()

import logging
import os

from app.engine.loaders import get_documents
from app.settings import init_settings
from app.engine.vectorstore import GoogleVertexVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def generate_datasource():
    init_settings()
    logger.info("Creating new index in Vertex AI Vector Search")
    
    # Load documents
    documents = get_documents()
    for doc in documents:
        doc.metadata["private"] = "false"
    
    # Create new index
    vector_store = GoogleVertexVectorStore()
    index = vector_store.create_index(documents)
    
    logger.info("Finished creating new index in Vertex AI Vector Search")


if __name__ == "__main__":
    generate_datasource()
