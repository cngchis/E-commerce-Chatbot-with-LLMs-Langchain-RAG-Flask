from flask import Flask, render_template, jsonify, request
from src.helper import load_embedding_model
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

model_file = "./model/vinallama-7b-chat_q5_0.gguf"

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embedding = load_embedding_model()

index_name = 'ecombot'

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":2})


# load LLM
llm = CTransformers(
    model=model_file, model_type="llama", max_new_tokens=128, temperature=0.01,
    config={
        "context_length": 1024
    }
)
prompt = PromptTemplate(input_variables=["context", "input"], template=system_prompt)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)