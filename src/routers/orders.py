import logging
from src.core.database import IDatabase

class OrdersRouter:
    def __init__(self, database: IDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def save_order(self, order_data: str) -> bool:
        if not isinstance(order_data, str):
            self.logger.error("Invalid order data. Order data must be a string.")
            return False

        try:
            if not self.database.is_connected():
                self.logger.error("Database connection is not established.")
                return False

            self.database.Save(order_data)
            self.logger.info("Order saved successfully.")
            return True
        except Exception as e:
            self.logger.error(f"An error occurred while saving the order: {str(e)}")
            return False