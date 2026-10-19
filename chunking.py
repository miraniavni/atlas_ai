def chunk_text(text, size, overlap):
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    step = size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start:start + size])
        if start + size >= len(text):
            break
    return chunks