from src.config.settings import Config
from src.core.database import DatabaseManager
from src.core.logger import setup_logger
from src.services.stock_service import StockService
from src.services.openai_service import OpenAIService
from src.services.rag_service import RAGService
from src.handlers.message_handler import MessageHandler
from src.bot.telegram_bot import TelegramBot

logger = setup_logger()
def main():
    try:
        config = Config()

        db_config = {
            "host": config.DB_HOST,
            "user": config.DB_USER,
            "password": config.DB_PASSWORD,
            "database": config.DB_NAME,
        }
        db_manager = DatabaseManager(db_config)
        
        stock_service = StockService(db_manager)
        openai_service = OpenAIService(config.OPENAI_API_KEY)
        rag_service = RAGService(documents_dir = config.DOCUMENTS_DIR, openai_api_key = config.OPENAI_API_KEY)
        
        message_handler = MessageHandler(stock_service, openai_service, rag_service)
        
        logger.info("Starting the bot...")
        telegram_bot = TelegramBot(
            token=config.TELEGRAM_TOKEN,
            command_handlers={},
            message_handlers=[message_handler.handle],
        )
        telegram_bot.run()
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()