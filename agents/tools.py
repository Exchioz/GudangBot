from langchain_core.tools import tool
from .handlers import ItemHandler, CompanyHandler

class AgentTools:
    """Class untuk mengelola tools yang digunakan oleh agent."""
    
    @staticmethod
    @tool
    def handle_item(item: str) -> str:
        """Mengecek informasi barang dalam database."""
        handler = ItemHandler()
        return handler.handle(item)
    
    @staticmethod
    @tool
    def handle_company(query: str) -> str:
        """Mengambil informasi tentang perusahaan dari RAG."""
        handler = CompanyHandler()
        return handler.handle(query)
    
    @classmethod
    def get_tools(cls) -> list:
        """Mengambil semua tools yang tersedia."""
        return [cls.handle_item, cls.handle_company]