import os
import logging
import streamlit as st
from app import app

## Set environment variables BEFORE any other imports
os.environ["USER_AGENT"] = "multi-agent-rag-app/1.0"
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"  # disables file watcher, fixes PyTorch event loop error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    st.title("Multi-Agent RAG App")
    question_input = st.text_input("Enter your question:")
    clear = st.button("Clear Results")

    if clear:
        st.experimental_rerun()

    if question_input:
        st.subheader("Workflow Execution")
        inputs = {"question": question_input}
        final_documents = []

        with st.spinner("Processing your question..."):
            try:
                for output in app.stream(inputs):
                    for node_name, node_data in output.items():
                        with st.expander(f"Node: `{node_name}`", expanded=True):
                            docs = node_data.get("documents", [])
                            # Show top 3 only for vectorstore, all for wiki_search
                            if docs:
                                if node_name == "vectorstore":
                                    top_docs = docs[:3]
                                else:
                                    top_docs = docs
                                for i, doc in enumerate(top_docs, start=1):
                                    if isinstance(doc, str):
                                        st.markdown(f"**Document {i}:** {doc}")
                                    elif isinstance(doc, dict):
                                        content = doc.get("page_content", "") or str(doc)
                                        st.markdown(f"**Document {i}:** {content}")
                                        if "metadata" in doc:
                                            st.caption(f"Metadata: {doc['metadata']}")
                                    else:
                                        st.markdown(f"**Document {i}:** {str(doc)}")
                                # Save only vectorstore top docs for final results
                                if node_name == "vectorstore":
                                    final_documents = top_docs
                            else:
                                st.info("No documents returned at this node.")
            except Exception as e:
                logger.error(f"Error during workflow execution: {e}")
                st.error(f"An error occurred: {e}")

        if final_documents:
            st.subheader("📄 Final Top 3 Results")
            for i, doc in enumerate(final_documents, start=1):
                if isinstance(doc, str):
                    st.markdown(f"**Result {i}:** {doc}")
                elif isinstance(doc, dict):
                    content = doc.get("page_content", "") or str(doc)
                    st.markdown(f"**Result {i}:** {content}")
                else:
                    st.markdown(f"**Result {i}:** {str(doc)}")

if __name__ == "__main__":
    main()
