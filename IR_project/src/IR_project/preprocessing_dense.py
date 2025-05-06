# hybrid retrieval: lexical and semantic
# step 1: implement lexical search

# NER?
# Normalization: 3pm - 3h - 15:00
# tokenization?
# n-grams?

# 1. Chunk long text
# sentence-based (spacy) or overlap for context preservation?
#
# 2. Clean text
#
# 3. Add metadata
#
# 4. Store results


from typing import List, Dict


def chunk_text(text: str, chunk_size: int=200, overlap: int=50) -> List[str]:
    """Splits text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap       # move start forward

    return chunks


def chunk_dataset_dense(chapter_data: List[Dict], chunk_size: int=200, overlap: int=50) -> List[Dict]:
    """Applies chunking to a list of chapter entries from the JSONL."""
    chunked_data_dense = []

    for entry in chapter_data:
        text_chunks = chunk_text(entry["text"], chunk_size, overlap)

        for i, chunk in enumerate(text_chunks):
            chunked_data_dense.append({
                "book": entry["book"],
                "book_number": entry["book_number"],
                "chapter_str_number": entry["chapter_str_number"],
                "chapter_int_number": entry["chapter_int_number"],
                "chapter_title": entry["chapter_title"],
                "chunk_index": i,
                "chunk_text": chunk
            })

    return chunked_data_dense





