from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import logging
import os

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, documents_dir: str, openai_api_key: str):
        self.documents_dir = documents_dir
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(
            base_url = "https://api.openai.com/v1/",
            api_key=openai_api_key,
            temperature=0.7
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            openai_api_base="https://api.openai.com/v1/"
        )
        self.vectorstore = self._load_documents()

    def _load_documents(self):
        try:
            loader = TextLoader("data\documents\data.txt")
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=250, 
                chunk_overlap=50
            )
            texts = text_splitter.split_documents(documents)
            return FAISS.from_documents(texts, self.embeddings)
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise

    def query(self, question: str) -> str:
        try:
            docs = self.vectorstore.similarity_search(question, k=2)
            context = "\n".join([doc.page_content for doc in docs])
            
            prompt = f"""
            Anda adalah asisten yang ramah. Jawab pertanyaan pengguna dengan informasi berikut:
            
            Konteks:
            {context}
            
            Pertanyaan:
            {question}
            
            Aturan:
            1. Gunakan bahasa Indonesia yang sopan dan informatif
            2. Jika informasi tidak ditemukan, jelaskan dengan ramah
            3. Berikan informasi yang akurat dan relevan
            4. Jangan memberikan informasi di luar konteks yang tersedia
            """
            
            response = self.llm(prompt)
            return response
        except Exception as e:
            logger.error(f"Error querying RAG system: {e}")
            raise