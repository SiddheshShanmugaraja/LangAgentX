import os
import logging
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY not found in environment variables.")

# Define schema
class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "wiki_search"] = Field(
        ..., description="Route question to either vectorstore or wikipedia"
    )

# Setup LLM
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")
structured_llm_router = llm.with_structured_output(RouteQuery)

# Routing prompt
system_prompt = (
    "You are an expert at routing user questions. "
    "Use vectorstore for questions about agents, prompt engineering, and adversarial attacks. "
    "Otherwise, use Wikipedia."
)
route_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}"),
])

# Final router chain
question_router = route_prompt | structured_llm_router