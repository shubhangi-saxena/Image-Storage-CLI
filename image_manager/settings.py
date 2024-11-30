from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

DATABASE_URL = "postgresql://username:password@hostname/dbname"  # Update with your credentials

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
