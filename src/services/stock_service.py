from typing import Optional, List
from src.models.stock import Stock
from src.core.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class StockService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def check_stock(self, item: str) -> Optional[Stock]:
        try:
            query = """
                SELECT item, quantity, price, category, description 
                FROM stocks 
                WHERE LOWER(item) = %s
            """
            result = self.db_manager.execute_query(query, (item.lower(),))
            
            if result:
                return Stock(
                    item=result[0],
                    quantity=result[1],
                    price=result[2],
                    category=result[3],
                    description=result[4]
                )
            return None
        except Exception as e:
            logger.error(f"Error checking stock for item {item}: {e}")
            raise