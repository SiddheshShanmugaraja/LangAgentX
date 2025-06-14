import logging
from typing import List, Dict, Any
from typing_extensions import TypedDict
from router import question_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]

def route_question(state: Dict[str, Any]) -> str:
    logger.info("---ROUTE QUESTION---")
    question = state.get("question", "")
    if not question:
        logger.warning("No question provided in state.")
        return "unknown"
    try:
        source = question_router.invoke({"question": question})
        if source.datasource == "wiki_search":
            logger.info("---ROUTE TO WIKI SEARCH---")
            return "wiki_search"
        elif source.datasource == "vectorstore":
            logger.info("---ROUTE TO VECTORSTORE---")
            return "vectorstore"
        else:
            logger.warning(f"Unknown datasource: {source.datasource}")
            return "unknown"
    except Exception as e:
        logger.error(f"Error in routing question: {e}")
        return "unknown"