from src.core.database import DatabaseConnection
from logging import getLogger

logger = getLogger(__name__)

def get_db_connection():
    try:
        db_connection = DatabaseConnection(
            db_host='localhost',
            db_port=5432,
            db_username='username',
            db_password='password',
            db_name='database'
        )
        return db_connection
    except Exception as e:
        logger.error(f"An error occurred while creating a database connection: {str(e)}")
        raise