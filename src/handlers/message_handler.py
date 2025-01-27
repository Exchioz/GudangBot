import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.services.stock_service import StockService
from src.services.openai_service import OpenAIService
from src.services.rag_service import RAGService

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(
        self,
        stock_service: StockService,
        openai_service: OpenAIService,
        rag_service: RAGService
    ):
        self.stock_service = stock_service
        self.openai_service = openai_service
        self.rag_service = rag_service

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await self.handle_message(update, context)
        except Exception as e:
            logger.error(f"Error in message handler: {e}")
            await update.message.reply_text(
                "Maaf, terjadi kesalahan. Silakan coba lagi."
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        
        try:
            response = self.openai_service.create_completion(
                messages=[{"role": "user", "content": user_input}],
                functions=[
                    {
                        "name": "check_stock",
                        "description": "Cek stok barang berdasarkan nama barang.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "item": {
                                    "type": "string",
                                    "description": "Nama barang yang ingin dicek stoknya.",
                                }
                            },
                            "required": ["item"],
                        },
                    },
                    {
                        "name": "company_info",
                        "description": "Cari informasi seputar perusahaan.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                ]
            )

            if response.choices[0].message.function_call:
                function_name = response.choices[0].message.function_call.name
                if function_name == "check_stock":
                    await self._handle_stock_query(update, response)
                else:
                    await self._handle_company_info(update, user_input)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            raise

    async def _handle_stock_query(self, update: Update, response: any):
        args = json.loads(response.choices[0].message.function_call.arguments)
        item = args.get("item")
        
        if not item:
            await update.message.reply_text(
                "Mohon sebutkan nama barang yang ingin dicek stoknya."
            )
            return
            
        stock = self.stock_service.check_stock(item)
        if stock:
            prompt = f"""
            Anda adalah asisten yang ramah. Berikan informasi stok barang dengan bahasa yang sopan dan informatif.
            Data stok:
            - Nama barang: {stock.item}
            - Stok tersedia: {stock.quantity} unit
            - Harga: {stock.price if stock.price else 'Tidak tersedia'}
            - Kategori: {stock.category if stock.category else 'Tidak tersedia'}
            - Deskripsi: {stock.description if stock.description else 'Tidak tersedia'}
            """
            chat_response = self.openai_service.create_completion(
                messages=[{"role": "user", "content": prompt}]
            )
            await update.message.reply_text(
                chat_response.choices[0].message.content
            )
        else:
            await update.message.reply_text(
                f"Maaf, barang {item} tidak ditemukan dalam sistem kami."
            )
    
    async def _handle_company_info(self, update: Update, user_input: str):
        response = self.rag_service.query(user_input)
        await update.message.reply_text(response)