from fastapi import FastAPI
from app.database import Base, engine
from app.routers import ingest, chat

Base.metadata.create_all(bind=engine)  # creates sqlite tables on first run

app = FastAPI(title="PalmMind RAG Backend")
app.include_router(ingest.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Chat"])

@app.get("/")
def root():
    return {"status": "running"}