import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, config: dict[str, str]):
        self.config = config
        
    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    def execute_query(self, query: str, params: tuple = None) -> any:
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except Error as e:
            logger.error(f"Query execution error: {e}")
            raise
        finally:
            conn.close()

    def execute_query_many(self, query: str, params: tuple = None) -> list[any]:
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            logger.error(f"Query execution error: {e}")
            raise
        finally:
            conn.close()