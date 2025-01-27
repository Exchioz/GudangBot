import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Dict, List, Callable, Coroutine, Any

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(
        self,
        token: str,
        command_handlers: Dict[str, Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]],
        message_handlers: List[Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]]
    ):
        self.token = token
        self.command_handlers = command_handlers
        self.message_handlers = message_handlers
        self.application = Application.builder().token(self.token).build()

    def setup_handlers(self):
        for command, handler in self.command_handlers.items():
            self.application.add_handler(CommandHandler(command, handler))

        for handler in self.message_handlers:
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    def run(self):
        self.setup_handlers()
        logger.info("Bot is starting...")
        self.application.run_polling()