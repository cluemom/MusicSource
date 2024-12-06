import sqlite3
import psycopg
from psycopg import sql
import pandas as pd
import sys
from typing import List, Tuple
import logging

# This was a tool used to transition from a sqlite db to postgres for prod. 
# This is saved here just in case it's needed in the future

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def get_sqlite_tables(sqlite_conn) -> List[str]:
    """Get all table names from SQLite database."""
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def get_table_schema(sqlite_conn, table_name: str) -> List[Tuple]:
    """Get schema information for a given table."""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()

def create_postgres_table(pg_conn, table_name: str, schema: List[Tuple]):
    """Create a PostgreSQL table based on the SQLite schema."""
    columns = []
    for column in schema:
        name = column[1]
        data_type = column[2]
        # Map SQLite types to PostgreSQL types
        pg_type = (
            "TEXT" if "CHAR" in data_type or "TEXT" in data_type else
            "INTEGER" if "INT" in data_type else
            "REAL" if "REAL" in data_type or "FLOAT" in data_type else
            "NUMERIC" if "NUM" in data_type else
            "BOOLEAN" if "BOOL" in data_type else
            "BYTEA" if "BLOB" in data_type else
            "TEXT"
        )
        columns.append(f"{name} {pg_type}")

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    with pg_conn.cursor() as cur:
        cur.execute(create_table_query)
        pg_conn.commit()

def insert_data_to_postgres(pg_conn, table_name: str, chunk: pd.DataFrame):
    """Insert a pandas DataFrame chunk into a PostgreSQL table."""
    with pg_conn.cursor() as cur:
        columns = chunk.columns.tolist()
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        cur.executemany(insert_query, chunk.values.tolist())
        pg_conn.commit()

def sqlite_to_postgres(
    sqlite_path: str,
    pg_host: str,
    pg_database: str,
    pg_user: str,
    pg_password: str,
    pg_port: int = 5432,
    chunk_size: int = 10000
):
    logger = setup_logging()

    try:
        # Connect to SQLite
        logger.info(f"Connecting to SQLite database: {sqlite_path}")
        sqlite_conn = sqlite3.connect(sqlite_path)

        # Connect to PostgreSQL
        logger.info(f"Connecting to PostgreSQL database: {pg_database}")
        pg_conn = psycopg.connect(
            host=pg_host,
            dbname=pg_database,
            user=pg_user,
            password=pg_password,
            port=pg_port
        )

        # Get all tables from SQLite
        tables = get_sqlite_tables(sqlite_conn)
        logger.info(f"Found {len(tables)} tables to migrate")

        for table in tables:
            logger.info(f"Migrating table: {table}")

            # Get table schema
            schema = get_table_schema(sqlite_conn, table)
            logger.info(f"Schema for {table}: {len(schema)} columns")

            # Create PostgreSQL table
            create_postgres_table(pg_conn, table, schema)

            # Read data in chunks using pandas
            chunks = pd.read_sql_query(
                f"SELECT * FROM {table}",
                sqlite_conn,
                chunksize=chunk_size
            )

            rows_migrated = 0

            for chunk in chunks:
                insert_data_to_postgres(pg_conn, table, chunk)
                rows_migrated += len(chunk)
                logger.info(f"Migrated {rows_migrated} rows for table {table}")

        logger.info("Migration completed successfully")

    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    sqlite_to_postgres(
        sqlite_path="db.sqlite3",
        pg_host="localhost",
        pg_database="musicsource_db",
        pg_user="sterfry",
        pg_password="Beanz123"
    )
