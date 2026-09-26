import json
from upstash_redis import Redis
from app.config import settings

redis = Redis(url=settings.redis_url, token=settings.redis_token)
HISTORY_LIMIT = 6  # last 6 turns is enough context without bloating the prompt

#history limit le last 6 turns ko context matra rakheko cha kinaki 6 turns ko context le chai enough context provide garxa
# jasko karan le prompt lai bloating(bloating means: making the prompt unnecessarily long) bata bachaucha.

def get_history(session_id: str) -> list[dict]:
    raw = redis.get(session_id)
    return json.loads(raw) if raw else []

def add_turn(session_id: str, role: str, content: str):
    history = get_history(session_id)
    history.append({"role": role, "content": content})
    redis.set(session_id, json.dumps(history[-HISTORY_LIMIT:]))
'''def ko through fuction define gareko cha jasma get_history le session_id ko through history fetch garxa ani
 add_turn le new turn add garxa :turn vaneko euta question ani answer ko pair ho jasma role vaneko chai user or chatbot 
 ho ani content vaneko chai user ko question or chatbot ko answer ho.'''