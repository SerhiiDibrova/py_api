from abc import ABC, abstractmethod
import psycopg2
from src.core.dependencies import get_db_config

class IDatabase(ABC):
    @abstractmethod
    def Save(self, data: str) -> None:
        pass

class DatabaseConnection(IDatabase):
    def __init__(self, db_config):
        self.db_config = db_config
        self.db_connection = None
        self.connect()

    def connect(self):
        try:
            self.db_connection = psycopg2.connect(
                host=self.db_config['host'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
        except psycopg2.Error as e:
            print(f"Failed to connect to database: {e}")

    def Save(self, data: str) -> None:
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("INSERT INTO table_name (data) VALUES (%s)", (data, ))
                self.db_connection.commit()
                cursor.close()
            except psycopg2.Error as e:
                print(f"Failed to save data to database: {e}")
        else:
            print("Database connection is not established")

def get_db_connection():
    db_config = get_db_config()
    return DatabaseConnection(db_config)