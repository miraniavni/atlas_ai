import pytest

from chunking import chunk_text


def test_short_text_is_one_chunk():
    assert chunk_text("hello world", size=50, overlap=10) == ["hello world"]

def test_long_text_is_split():
    text = "abcdefghij" *10
    chunks = chunk_text(text, size=40, overlap=10)
    assert len(chunks) > 1
    assert all(len(c) <=40 for c in chunks)

def test_chunks_overlap():
    text = "abcdefghij"*10
    chunks = chunk_text(text, size=40, overlap=10)
    assert chunks[0][-10:] == chunks[1][:10]
def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunk_text("hello world", size=10, overlap=10)

def test_no_redundant_last_chunk():
    chunks = chunk_text("abcdefghij" * 10, size=40, overlap=10)
    assert len(chunks) == 3


def test_empty_text_gives_no_chunks():
    assert chunk_text("", size=40, overlap=10) == []
