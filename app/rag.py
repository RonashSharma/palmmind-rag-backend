import google.generativeai as genai
from app.config import settings
from app.embeddings import embed_texts
from app.vectorstore import search
from app.memory import get_history, add_turn

genai.configure(api_key=settings.gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")
#yo build prompt function le chai user ko query, context chunks, ani history lai prompt ma assemble garxa
#  jasma conversation so far, context from the document, ani question vanera clearly mention garxa.
def build_prompt(query: str, context_chunks: list[str], history: list[dict]) -> str:
    # manual prompt assembly — this is what replaces RetrievalQAChain
    history_text = "\n".join(f"{h['role']}: {h['content']}" for h in history)
    context_text = "\n---\n".join(context_chunks)
    return (
        f"You are a helpful assistant answering questions using the context below.\n\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"Context from the document:\n{context_text}\n\n"
        f"Question: {query}\nAnswer clearly and only from the context above:"
    )
#yo function answer_query le chai user ko query lai answer garxa jasma session_id ko through history fetch garxa 
# ani query lai embed garera vector ma convert garxa ani search function ko through context chunks fetch garxa 
# ani build_prompt function ko through prompt build garxa tespaxi llm.generate_content ko through response generate garxa 
# ani add_turn function ko through user ko query ani assistant ko response lai memory ma add garxa ani finally response text return garxa.
def answer_query(session_id: str, query: str) -> str:
    history = get_history(session_id)
    query_vector = embed_texts([query])[0]
    context_chunks = search(query_vector)
    prompt = build_prompt(query, context_chunks, history)
    response = llm.generate_content(prompt)
    add_turn(session_id, "user", query)
    add_turn(session_id, "assistant", response.text)
    return response.text