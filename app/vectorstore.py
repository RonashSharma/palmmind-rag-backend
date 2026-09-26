import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings

client = QdrantClient(path=settings.qdrant_path)
COLLECTION = "palmmind_docs"

def ensure_collection(vector_size: int = 384):
    if COLLECTION not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_chunks(document_id: str, chunks: list[str], vectors: list[list[float]]):
    ensure_collection()
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vectors[i], payload={"document_id": document_id, "text": chunks[i]})
        for i in range(len(chunks))
    ]
    client.upsert(collection_name=COLLECTION, points=points)

def search(query_vector: list[float], top_k: int = 4) -> list[str]:
    ensure_collection()
    results = client.search(collection_name=COLLECTION, query_vector=query_vector, limit=top_k)
    return [r.payload["text"] for r in results]