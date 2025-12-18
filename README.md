# E-commerce-Chatbot-with-LLMs-Langchain-RAG-Flask

# How to run?
### STEPS:

Clone the repository

```bash
git clone https://github.com/cngchis/E-commerce-Chatbot-with-LLMs-Langchain-RAG-Flask
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n ecombot python=3.12 -y
conda activate ecombot
```
### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```
### STEP 03 - install the models into folder model
llm (vinallama-7b-chat-GGUF) - https://huggingface.co/vilm/vinallama-7b-chat-GGUF/tree/main
embedding model (/all-MiniLM-L6-v2-f16.gguf) - https://huggingface.co/caliex/all-MiniLM-L6-v2-f16.gguf/tree/main

### Create a .env file in the root directory and add your Pinecone & openai credentials as follows:
```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```

### Techstack Used:

- Python
- LangChain
- Flask
- Pinecone