import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///example.db")

# Ensure efficient connection handling, especially for SQLite
engine_options = {}
if DATABASE_URL.startswith("sqlite://"):
    engine_options = {"connect_args": {"check_same_thread": False}, "pool_pre_ping": True}

engine = create_engine(
    DATABASE_URL, 
    **engine_options
)

# Optimize session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Keeps objects available after commit
)

db_session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    return db_session

def close_db_session(exception=None):
    db_session.remove()