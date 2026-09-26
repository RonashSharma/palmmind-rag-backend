import io
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.database import get_db
from app.models import DocumentRecord
from app.chunking import get_chunks
from app.embeddings import embed_texts
from app.vectorstore import upsert_chunks
from app.schemas import IngestResponse

router = APIRouter()

def extract_text(file: UploadFile) -> str:
    content = file.file.read()
    if file.filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return content.decode("utf-8")

@router.post("/ingest", response_model=IngestResponse)
def ingest_document(
    file: UploadFile = File(...),
    strategy: str = Form("fixed"),
    db: Session = Depends(get_db),
):
    text = extract_text(file)
    chunks = get_chunks(text, strategy)
    vectors = embed_texts(chunks)

    document_id = str(uuid.uuid4())
    upsert_chunks(document_id, chunks, vectors)

    db.add(DocumentRecord(id=document_id, filename=file.filename, chunk_strategy=strategy, chunk_count=len(chunks)))
    db.commit()

    return IngestResponse(document_id=document_id, chunk_count=len(chunks), strategy_used=strategy)