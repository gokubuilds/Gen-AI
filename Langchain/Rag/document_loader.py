import tempfile

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


def document_loader(file_path):
    if hasattr(file_path, "read"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(file_path.read())
            temp_path = tmp.name
        pdf_path = temp_path
    else:
        pdf_path = str(file_path)

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        add_start_index=True,
    )

    all_splits = text_splitter.split_documents(docs)
    return all_splits
