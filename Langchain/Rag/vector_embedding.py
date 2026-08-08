import os

from dotenv import load_dotenv
from google.genai import Client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from Langchain.Rag.document_loader import document_loader

load_dotenv()

api_key = os.getenv("gemini_api") or os.getenv("GEMINI_API_KEY")

client = QdrantClient(url="http://localhost:6333")
embeddings = None
qdrant = None


def ensure_collection(collection_name="RAG_DEMO"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE,
            ),
        )
    return client


def init_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            google_api_key=api_key,
        )
    return embeddings


def index_pdf_to_qdrant(file_path, collection_name="RAG_DEMO"):
    global qdrant
    ensure_collection(collection_name)
    docs = document_loader(file_path)
    emb = init_embeddings()
    qdrant = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=emb,
        url="http://localhost:6333",
        collection_name=collection_name,
    )
    return qdrant


def retrive(query):
    global qdrant
    if qdrant is None:
        raise RuntimeError("No PDF has been uploaded yet. Please upload a PDF first.")
    return qdrant.similarity_search(query, k=4)


