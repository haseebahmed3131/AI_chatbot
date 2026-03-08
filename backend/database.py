from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file
root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)

# MySQL Database Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "supportlens_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "supportlens_db")

# Construct MySQL connection URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CategoryEnum(str, enum.Enum):
    BILLING = "Billing"
    REFUND = "Refund"
    ACCOUNT_ACCESS = "Account Access"
    CANCELLATION = "Cancellation"
    GENERAL_INQUIRY = "General Inquiry"

class Trace(Base):
    __tablename__ = "traces"
    
    id = Column(String(36), primary_key=True, index=True)  # UUID length
    user_message = Column(String(2000), nullable=False)  # Max 2000 chars
    bot_response = Column(String(2000), nullable=False)  # Max 2000 chars
    category = Column(String(50), nullable=False)  # Category name length
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, nullable=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
