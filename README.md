# PalmMind RAG Backend

A FastAPI backend with two APIs: document ingestion (PDF/TXT → chunked → embedded → stored in Qdrant)
and a conversational RAG API (custom retrieval, Redis-backed multi-turn memory, and LLM-driven
interview booking).

## Stack

- **FastAPI** : web framework, typed request/response models via Pydantic
- **sentence-transformers** (`all-MiniLM-L6-v2`) : local embeddings, no API key, no rate limit
- **Qdrant** : vector store, running in local file mode (no server/Docker required)
- **SQLite + SQLAlchemy** : document metadata and booking storage
- **Redis** (Upstash free tier) : per-session chat memory
- **Gemini API** (`gemini-2.5-flash-lite`) : answer generation, query rewriting, and booking field extraction

## Setup

1. Clone the repo and enter it:
   ```
   git clone <repo-url> && cd palmmind-rag-backend
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv pmenv
   source pmenv/bin/activate      # Windows: pmenv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your own keys:
   - `GEMINI_API_KEY` : from https://aistudio.google.com/apikey
   - `REDIS_URL` / `REDIS_TOKEN` : from https://upstash.com → create a free Redis DB → REST API tab

5. Run the server:
   ```
   uvicorn app.main:app
   ```
   (avoid `--reload` if you hit a Qdrant file-lock error : local file-mode Qdrant only allows
   one process to hold the storage folder at a time)

6. Open `http://127.0.0.1:8000/docs` to try both endpoints interactively.

## Endpoints

### `POST /ingest`
- `file`: PDF or TXT file
- `strategy`: `"fixed"` (character window with overlap) or `"sentence"` (groups whole sentences)
- Returns `document_id`, `chunk_count`, `strategy_used`

### `POST /chat`
- `session_id`: any string, used to track conversation memory
- `query`: a question about an ingested document, or a booking request
- Returns `answer`, `booking_captured`

If the query is a booking request (contains booking-intent keywords), the endpoint short-circuits:
it extracts name/email/date/time via the LLM, saves it, and returns a confirmation message :
it does not run RAG on booking messages.

If the query is a normal question, it's rewritten against the last few turns of chat history
(so follow-ups like "can you go deeper on that?" resolve correctly) before being embedded and
searched against Qdrant.

## Design notes

- Retrieval and prompt assembly are hand-written in `app/rag.py` : no LangChain `RetrievalQAChain`.
- Vector storage uses Qdrant's local file mode, not FAISS or Chroma.
- Chat history is stored in Redis per `session_id`, trimmed to the last 6 turns.
- Booking detection is a keyword check; extraction asks the LLM for strict JSON, validated before saving.
- No email is actually sent on booking : the confirmation message is informational only, and the
  booking is persisted to SQLite. Wiring a real email service would be the natural next step.
- No UI was built : this is a backend-only submission, tested via `/docs` and `curl`.

## Known limitation

Vague, broad questions (e.g. "what is this document about?") can retrieve front-matter/boilerplate
chunks over the actual content, since generic questions embed close to generic text. Specific
questions retrieve accurately. This is a known characteristic of similarity-based retrieval, not
a defect in the pipeline.

## Testing this repo

```bash
# ingest a document
curl -X POST http://127.0.0.1:8000/ingest -F "file=@sample.pdf" -F "strategy=fixed"

# ask a question
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "query": "What does the document say about X?"}'

# ask a follow-up
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "query": "Can you go deeper on that?"}'

# trigger a booking
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "query": "Book me an interview, I am Jane Doe [name anything here], email jane@example.com, on 2026-10-05 at 2pm"}'
```