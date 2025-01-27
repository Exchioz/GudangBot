from dataclasses import dataclass
from dotenv import load_dotenv
import os

@dataclass
class Config:
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
        self.OPENAI_BASE_URL: str = os.getenv("OPEBAU_BASE_URL")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.DB_HOST: str = os.getenv("DB_HOST")
        self.DB_USER: str = os.getenv("DB_USER")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        self.DB_NAME: str = os.getenv("DB_NAME")
        self.DOCUMENTS_DIR: str = os.getenv("DOCUMENTS_DIR")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")