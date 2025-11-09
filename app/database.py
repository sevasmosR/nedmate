# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

DB_USER = "nedmateadmin"
DB_PASS = urllib.parse.quote_plus("SecretP@ssword1")  # encode special chars
DB_HOST = "nedmate-ai-db-001.postgres.database.azure.com"
DB_PORT = 5432
DB_NAME = "postgres"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # echo=True prints SQL queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
