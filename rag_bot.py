import os
import pickle
import requests
import faiss

from typing import Optional, List
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
import dotenv

dotenv.load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


vectorstore = None

class GroqLLM(LLM):
    api_key: str  # Define api_key as a field
    model: str = "compound-beta"
    temperature: float = 0.2

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
        }

        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status() # This will raise the HTTPError for 400, 500 etc.
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
           
            if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
                try:
                    error_details = e.response.json()
                    return f"[Error: {e}] - Details: {error_details}"
                except json.JSONDecodeError:
                    return f"[Error: {e}] - Response body: {e.response.text}"
            else:
                return f"[Error: {str(e)}]"

    @property
    def _llm_type(self) -> str:
        return "groq_llm"


# 🔍 PDF Processing & FAISS Index Creation
def process_pdf(filepath: str) -> str: # Removed api_key as it's not needed for embedding
    global vectorstore

    loader = PyPDFLoader(filepath)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(chunks, embedding_model)

    with open("faiss_store.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

    return f"Processed {len(chunks)} chunks"


# ❓ Answer a Question via LangChain + Groq LLM
def get_answer(question: str, api_key: str) -> dict:
    global vectorstore

    if not vectorstore:
        if os.path.exists("faiss_store.pkl"):
            with open("faiss_store.pkl", "rb") as f:
                vectorstore = pickle.load(f)
        else:
            return {"error": "FAISS index not found. Please upload a PDF first."}

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    groq_llm = GroqLLM(api_key=api_key)

    qa = RetrievalQA.from_chain_type(llm=groq_llm, retriever=retriever, return_source_documents=True)
    result = qa({"query": question})

    return {
        "answer": result["result"]
    }

