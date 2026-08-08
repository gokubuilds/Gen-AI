import tempfile

import streamlit as st

from Langchain.Rag.retriver_model import llm_call
from Langchain.Rag.vector_embedding import index_pdf_to_qdrant, retrive

st.set_page_config(page_title="PDF RAG Chatbot", page_icon="📄")
st.title("PDF RAG CHATBOT")

uploaded_file = st.file_uploader(" Upload a PDF file ", type=["pdf"])

if uploaded_file is not None:
    if "pdf_path" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            st.session_state["pdf_path"] = tmp.name
            st.session_state["pdf_name"] = uploaded_file.name

    if st.button("Upload PDF to Qdrant"):
        with st.spinner("Indexing PDF into Qdrant..."):
            try:
                index_pdf_to_qdrant(st.session_state["pdf_path"])
                st.success("PDF uploaded and indexed successfully.")
            except Exception as exc:
                st.error(f"Failed to index PDF: {exc}")

prompt = st.chat_input("Enter your query")
if prompt:
    if "pdf_path" not in st.session_state:
        st.warning("Please upload a PDF first.")
    else:
        try:
            search_results = retrive(prompt)
            context_text = "\n\n".join([chunk.page_content for chunk in search_results])
            response = llm_call(prompt, context_text)
            st.write(response)
        except Exception as exc:
            st.error(f"Query failed: {exc}")
