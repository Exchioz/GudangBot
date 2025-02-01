from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import os

class CompanyHandler:
    def __init__(self,
        client_embed: OpenAIEmbeddings,
        vector_store_path: str = 'data/faiss_index',
        document_path: str = 'data/resource.txt',
    ):
        self.client_embed = client_embed
        self.document_path = document_path
        self.vector_store_path = vector_store_path
        self.vector_store = self.__load_vector_store()

    def handle(self, query: str) -> str:
        if self.vector_store is None:
            documents = self.__chunk_doc(self.document_path)
            self.vector_store = FAISS.from_documents(documents, self.client_embed)
            self.__save_vector_store()

        return self.__search(query)

    def __search(self, query: str):
        results = self.vector_store.similarity_search(query, k=3)
        if results:
            return "\n\n".join([result.page_content for result in results])
        else:
            return "Tidak ada informasi relevan ditemukan."

    def __chunk_doc(self, chunk_size: int = 500, chunk_overlap: int = 150):
        if not os.path.exists(self.document_path):
            raise FileNotFoundError(f"File {self.document_path} tidak ditemukan.")
        
        loader = TextLoader(self.document_path)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_documents(document)

    def __load_vector_store(self):
        if os.path.exists(self.vector_store_path):
            return FAISS.load_local(self.vector_store_path, self.client_embed, allow_dangerous_deserialization=True)
        return None

    def __save_vector_store(self):
        self.vector_store.save_local(self.vector_store_path)