from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from src.helper import extract_data_from_pdf, extract_data_from_csv, filter_to_minimal_docs, text_split, load_embedding_model

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

pdf_docs = extract_data_from_pdf("data/pdf")
csv_docs = extract_data_from_csv("data/csv")

pdf_docs=filter_to_minimal_docs(pdf_docs)
csv_docs=filter_to_minimal_docs(csv_docs)

texts_chunk = text_split(pdf_docs)

final_docs = texts_chunk+csv_docs

embedding = load_embedding_model()

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)

index_name = "ecombot"

if not pc.has_index(index_name):
    pc.create_index(
        index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        )
    )

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents=final_docs,
    embedding=embedding,
    index_name=index_name,
)