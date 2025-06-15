from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langgraph.graph import StateGraph, START, END

from tasks import route_question, GraphState
from agents import retrieve, wiki_search
from rag_utils import vector_store

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=0)
doc_splits = splitter.split_documents(docs_list)
vector_store.add_documents(doc_splits)

# Define retriever-based index
astra_vector_index = VectorStoreIndexWrapper(vectorstore=vector_store)

## Build graph
workflow = StateGraph(GraphState)
workflow.add_node("wiki_search", wiki_search)
workflow.add_node("retrieve", retrieve)

workflow.add_conditional_edges(
    START,
    route_question,
    {
        "wiki_search": "wiki_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("retrieve", END)
workflow.add_edge("wiki_search", END)
app = workflow.compile()