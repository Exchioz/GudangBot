import mysql.connector
from mysql.connector import Error

class DBConfig:
    def __init__(self, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_connection = None

    def connect(self):
        try:
            if self.db_connection is None or not self.db_connection.is_connected():
                self.db_connection = mysql.connector.connect(
                    host=self.db_host,
                    port=self.db_port,
                    user=self.db_user,
                    password=self.db_password,
                    database=self.db_name,
                    autocommit=True 
                )
        except Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            self.db_connection = None
            print("Database connection closed.")
        else:
            print("No active database connection.")

    def execute_query(self, query: str, params: tuple = ()) -> list:
        try:
            self.connect()
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            print(f"Query execution error: {e}")
            return []