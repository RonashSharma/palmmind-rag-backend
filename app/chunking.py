import re

def fixed_size_chunks(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    # sliding window so consecutive chunks share context and don't cut a sentence in half
    chunks = []
    start = 0
    while start < len(text): #start<len menas in short, keep creating chunks until the start index reaches the end of the text
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap #esma chai k hunxa vanda consecutive chunks ma overlap hunxa,
        # so start index is moved forward by size - overlap to create the next chunk
    return [c.strip() for c in chunks if c.strip()]
#c.strip() vaneko chai whitespace haru lai remove garne, ani if c.strip() vaneko chai empty string haru lai remove garne

def sentence_window_chunks(text: str, sentences_per_chunk: int = 5) -> list[str]:
    # groups whole sentences instead of raw characters, keeps meaning intact
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks

def get_chunks(text: str, strategy: str) -> list[str]:
    if strategy == "fixed":
        return fixed_size_chunks(text)
    if strategy == "sentence":
        return sentence_window_chunks(text)
    raise ValueError(f"Unknown chunking strategy: {strategy}")