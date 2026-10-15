"""
CampusAI - Database Connection Manager
Handles SQLite connection and session management using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database path - relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "campus_ai.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """Get a direct database session (non-generator)."""
    return SessionLocal()


def execute_raw_sql(sql_query: str):
    """
    Execute a raw SQL query and return results as list of dicts.
    Used by the NLP engine to run generated SQL queries.
    """
    with engine.connect() as conn:
        try:
            result = conn.execute(text(sql_query))
            if result.returns_rows:
                columns = list(result.keys())
                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                return {
                    "success": True,
                    "columns": columns,
                    "data": rows,
                    "row_count": len(rows)
                }
            else:
                return {
                    "success": True,
                    "columns": [],
                    "data": [],
                    "row_count": 0,
                    "message": "Query executed successfully (no results to return)."
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "columns": [],
                "data": [],
                "row_count": 0
            }


def get_table_names():
    """Return all table names in the database."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        return [row[0] for row in result.fetchall()]


def get_table_schema(table_name: str):
    """Return column info for a given table."""
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
        return [{"cid": r[0], "name": r[1], "type": r[2], "notnull": r[3], "default": r[4], "pk": r[5]}
                for r in result.fetchall()]
