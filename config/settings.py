from dataclasses import dataclass
import dotenv
import os

@dataclass
class Settings:
    def __init__(self):
        dotenv.load_dotenv()
        self.OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.OPENAI_LLM_MODEL: str = os.getenv("OPENAI_LLM_MODEL")
        # self.TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
        # self.DB_HOST: str = os.getenv("DB_HOST")
        # self.DB_USER: str = os.getenv("DB_USER")
        # self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        # self.DB_NAME: str = os.getenv("DB_NAME")
        # self.DOCUMENTS_DIR: str = os.getenv("DOCUMENTS_DIR")
        # self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.SYSTEM_PROMPT: str = "Anda merupakan sebuah ChatBot AI di sebuah perusahaan yang dimana hanya bisa ditugaskan untuk melakukan hal-hal yang berhubungan yang ada di perusahaan ini. Jika anda tidak memanggil tools, jangan jawab pertanyaanya dan tolak dengan baik."