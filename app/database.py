from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

MARIADB_USER = os.getenv("MARIADB_USER", "cruduser")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "crudpass")
MARIADB_HOST = os.getenv("MARIADB_HOST", "mariadb")
MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
MARIADB_DB = os.getenv("MARIADB_DB", "cruddemo")

DATABASE_URL = f"mariadb+mariadbconnector://{MARIADB_USER}:{MARIADB_PASSWORD}@{MARIADB_HOST}:{MARIADB_PORT}/{MARIADB_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
