from typing import Any, List, Mapping, Optional, Sequence, Union
import logging

import psycopg2
from psycopg2._psycopg import connection
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


ResultRow = Mapping[str, Any]
Params    = Union[Sequence[Any], Mapping[str, Any], None]


class DatabaseConnection:
    """Database connection class with context manager, rollback on error,
       and RealDictCursor-typing."""

    conn: connection

    def __init__(
        self,
        conn: Optional[connection] = None,
        dsn: Optional[str] = None,
        autocommit: bool = False
    ) -> None:
        self.conn = conn or psycopg2.connect(dsn, cursor_factory=RealDictCursor)
        self.conn.autocommit = autocommit

    def __enter__(self) -> "DatabaseConnection":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc:
            logger.exception("Exception occurred, rolling back transaction")
            self.conn.rollback()
        else:
            if not self.conn.autocommit:
                self.conn.commit()
        self.close()

    def query_all(
        self,
        query: str,
        params: Params = None
    ) -> List[ResultRow]:
        """Execute a query and return all rows as list of dicts"""
        logger.debug("Executing query_all: %s %s", query, params)
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def query_one(
        self,
        query: str,
        params: Params = None
    ) -> Optional[ResultRow]:
        """Execute a query and return a single row as dict"""
        logger.debug("Executing query_one: %s %s", query, params)
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def execute(
        self,
        query: str,
        params: Params = None
    ) -> None:
        """Execute a modifying query (INSERT/UPDATE/DELETE)"""
        logger.debug("Executing execute: %s %s", query, params)
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)

    def close(self) -> None:
        """Close the connection"""
        try:
            self.conn.close()
            logger.debug("Database connection closed")
        except Exception:
            logger.exception("Error closing the database connection")
