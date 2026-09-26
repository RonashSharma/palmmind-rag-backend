from pydantic import BaseModel

class IngestResponse(BaseModel):
    document_id: str
    chunk_count: int
    strategy_used: str

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    answer: str
    booking_captured: bool = False

'''yo file ma chai schemas haru define gareko cha, jasma IngestResponse,
 ChatRequest, ani ChatResponse classes haru cha.
 harek class ko xutai working xa jastai 
 ingestresponse: le k garxa vani document id, chunk count, ani strategy used lai response ma return garxa.
 chatrequest: le session id ani query lai request ma accept garxa.
 chatresponse: le answer ani booking captured lai response ma return garxa. booking captured ko default value false xa.'''