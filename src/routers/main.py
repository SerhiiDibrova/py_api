# src/routers/main.py

import logging
from src.core.coordinator import Coordinator

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

def main():
    logger = Logger()
    coordinator = Coordinator(logger)
    coordinator.Run()

if __name__ == "__main__":
    main()