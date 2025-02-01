from .prompt import Prompt

from dataclasses import dataclass
import dotenv
import os

@dataclass
class Settings:
    def __init__(self):
        dotenv.load_dotenv()
        self.COMPANY_NAME: str = os.getenv("COMPANY_NAME")
        self.OPENAI_API_URL: str = os.getenv("OPENAI_API_URL")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.OPENAI_LLM_MODEL: str = os.getenv("OPENAI_LLM_MODEL")
        self.OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL")
        self.SYSTEM_PROMPT: str = Prompt().get_prompt()
        self.DB_HOST: str = os.getenv("DB_HOST")
        self.DB_PORT: int = os.getenv("DB_PORT")
        self.DB_USER: str = os.getenv("DB_USER")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        self.DB_NAME: str = os.getenv("DB_NAME")
        # self.TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
        # self.DOCUMENTS_DIR: str = os.getenv("DOCUMENTS_DIR")
        # self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")