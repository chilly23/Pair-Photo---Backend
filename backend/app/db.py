from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Default to file-based sqlite for easy local dev. Use DATABASE_URL to override.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# echo=False for clean logs
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
