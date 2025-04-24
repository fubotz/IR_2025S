from typing import List, Dict
import spacy

nlp = spacy.load("en_core_web_sm")


def chunk_text_with_sentence_boundaries(text, max_words=200):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    chunks = []
    current_chunk = []
    word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())

        # If adding this sentence would exceed limit, save current chunk and start new
        if word_count + sentence_word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            word_count = sentence_word_count
        else:
            current_chunk.append(sentence)
            word_count += sentence_word_count

    # Add last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_dataset_bm25(chapter_data: List[Dict], max_words=200) -> List[Dict]:
    chunked_data_bm25 = []

    for entry in chapter_data:
        original_text = entry["text"]
        chunks = chunk_text_with_sentence_boundaries(original_text, max_words=max_words)

        for i, chunk in enumerate(chunks):
            chunked_entry = {
                "book": entry["book"],
                "book_number": entry["book_number"],
                "chapter_str_number": entry["chapter_str_number"],
                "chapter_int_number": entry["chapter_int_number"],
                "chapter_title": entry["chapter_title"],
                "chunk_index": i,
                "chunk_text": chunk
            }
            chunked_data_bm25.append(chunked_entry)

    return chunked_data_bm25