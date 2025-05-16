import sqlite3
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, db_name: str):
        if not db_name:
            raise ValueError("Database name is required")
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            logger.info("Database connection established")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def execute_query(self, query: str, params: Optional[tuple] = None):
        if not query:
            raise ValueError("Query is required")
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            logger.info("Query executed successfully")
        except sqlite3.Error as e:
            logger.error(f"Failed to execute query: {e}")
            raise

    def fetch_all(self, query: str, params: Optional[tuple] = None):
        if not query:
            raise ValueError("Query is required")
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            logger.info("Fetched data from database")
            return result
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch data: {e}")
            raise

    def close_connection(self):
        try:
            self.conn.close()
            logger.info("Database connection closed")
        except sqlite3.Error as e:
            logger.error(f"Failed to close database connection: {e}")
            raise


def get_db_connection(db_name: str) -> DatabaseConnection:
    if not db_name:
        raise ValueError("Database name is required")
    return DatabaseConnection(db_name)


class ReportGenerator:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def generate_report(self, query: str, params: Optional[tuple] = None):
        if not query:
            raise ValueError("Query is required")
        try:
            data = self.db_connection.fetch_all(query, params)
            # Generate report using the fetched data
            logger.info("Report generated successfully")
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            raise