# src/core/coordinator.py

import logging
from src.core.report_generator import ReportGenerator
from src.core.dependencies import get_db_connection

class Coordinator:
    def __init__(self):
        self.report_generator = ReportGenerator()
        self.db_connection = get_db_connection()

    def Run(self):
        logging.info('Start')
        self.report_generator.Generate(self.db_connection)
        logging.info('Done')