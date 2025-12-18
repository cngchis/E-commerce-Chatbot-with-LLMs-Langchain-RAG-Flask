from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain_community.embeddings import GPT4AllEmbeddings


# Extract data from pdf
def extract_data_from_pdf(data):
    loader = DirectoryLoader(data,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader
    )

    documents = loader.load()

    return documents
def extract_data_from_csv(data):
    loader = DirectoryLoader(
        data,
        glob="*.csv",
        loader_cls=CSVLoader,
        loader_kwargs={
            "encoding": "utf-8-sig",
            "csv_args": {
                "delimiter": ","
            }
        }
    )
    documents = loader.load()
    return documents
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of documents objects,return a new list of document objects
    containing only 'source' in the metadata and original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

# text splitter
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 512,
        chunk_overlap = 50
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk

def load_embedding_model():
    embedding = GPT4AllEmbeddings(model_file="./model/all-MiniLM-L6-v2-f16.gguf")
    return embedding