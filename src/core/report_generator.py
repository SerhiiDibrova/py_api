# src/core/report_generator.py

import logging
from src.core.database_connection import DatabaseConnection

class ReportGenerator:
    def Generate(self, db_connection: DatabaseConnection) -> None:
        try:
            logging.info("Start")
            data = db_connection.get_data()
            report = self.generate_report(data)
            self.save_report(report)
            logging.info("Done")
        except Exception as e:
            logging.error(f"Error generating report: {str(e)}")

    def generate_report(self, data):
        # Implement report generation logic here
        # For demonstration purposes, a simple report is generated
        report = "Report:\n"
        for item in data:
            report += f"{item}\n"
        return report

    def save_report(self, report):
        # Implement report saving logic here
        # For demonstration purposes, the report is printed to the console
        print(report)