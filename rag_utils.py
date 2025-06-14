import os
import logging
from dotenv import load_dotenv
import cassio
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not ASTRA_DB_APPLICATION_TOKEN or not ASTRA_DB_ID:
    logger.error("Missing Astra DB credentials in environment variables.")

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Cassandra(
    embedding=embeddings,
    table_name="qa_mini_demo"
)

retriever = vector_store.as_retriever()