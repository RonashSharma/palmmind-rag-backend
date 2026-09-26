from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.rag import answer_query
from app.booking import wants_booking, extract_booking_fields, save_booking

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    booking_captured = False
    if wants_booking(request.query):
        fields = extract_booking_fields(request.query)
        if fields and fields.get("email"):
            save_booking(request.session_id, fields)
            booking_captured = True

    answer = answer_query(request.session_id, request.query)
    return ChatResponse(answer=answer, booking_captured=booking_captured)