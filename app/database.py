from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
#session local creates a new session factory that will be used to create database sessions. 
# It is configured with the database URL from the settings and is set to not autocommit or autoflush changes to the database automatically.
#engine is the SQLAlchemy engine that manages the connection to the database specified in the settings.
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#get_db is used for dependency injection in FastAPI to provide a database session to route handlers. 
# It creates a new session, yields it for use, and ensures that the session is closed after the request is completed.
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()