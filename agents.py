import logging
from typing import Dict, Any, List
from langchain.schema import Document
from tools import wiki
from rag_utils import retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve documents from the vectorstore based on the question."""
    logger.info("---RETRIEVE---")
    question = state.get("question", "")
    if not question:
        logger.warning("No question provided in state.")
        return {"documents": [], "question": question}
    documents = retriever.invoke(question)
    if isinstance(documents, list):
        docs_list = documents
    else:
        docs_list = [documents]
    return {"documents": docs_list, "question": question}

def wiki_search(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve documents from Wikipedia based on the question."""
    logger.info("---WIKIPEDIA---")
    question = state.get("question", "")
    if not question:
        logger.warning("No question provided in state.")
        return {"documents": [], "question": question}
    docs = wiki.invoke({"query": question})
    if isinstance(docs, list):
        result_docs = [Document(page_content=doc) for doc in docs]
    else:
        result_docs = [Document(page_content=docs)]
    return {"documents": result_docs, "question": question}