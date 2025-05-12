import sqlite3
import math
from pathlib import Path
from collections import defaultdict


# add a base Retriever class to support hybrid retrieval?


class BM25RetrieverSQLite:
    def __init__(self, db_path, k1=1.5, b=0.75):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.k1 = k1
        self.b = b
        self.N = self._get_total_docs()
        self.avgdl = self._get_avg_doc_length()

    def _get_total_docs(self):
        result = self.conn.execute("SELECT COUNT(*) FROM chapters").fetchone()
        return result[0]

    def _get_avg_doc_length(self):
        result = self.conn.execute("SELECT AVG(doc_length) FROM chapters").fetchone()
        return result[0]

    def _get_document_frequency(self, token):
        result = self.conn.execute("""
            SELECT document_frequency FROM vocabulary WHERE token = ?
        """, (token,)).fetchone()
        return result[0] if result else 0

    def _get_postings(self, token):
        rows = self.conn.execute("""
            SELECT chapter_id, frequency FROM inverted_index WHERE token = ?
        """, (token,)).fetchall()
        return rows     # list of (chapter_id, frequency)

    def _get_doc_lengths(self, chapter_ids):
        placeholders = ",".join("?" for _ in chapter_ids)
        query = f"SELECT chapter_id, doc_length FROM chapters WHERE chapter_id IN ({placeholders})"
        rows = self.conn.execute(query, tuple(chapter_ids)).fetchall()
        return {cid: length for cid, length in rows}

    def rank(self, query_tokens, top_n=5):
        scores = defaultdict(float)
        doc_lengths = {}

        for token in query_tokens:
            df = self._get_document_frequency(token)
            if df == 0:
                continue

            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
            postings = self._get_postings(token)
            chapter_ids = [cid for cid, _ in postings]

            if not doc_lengths:
                doc_lengths = self._get_doc_lengths(set(chapter_ids))

            for chapter_id, freq in postings:
                dl = doc_lengths.get(chapter_id, self.avgdl)
                tf_component = (freq * (self.k1 + 1)) / (freq + self.k1 * (1 - self.b + self.b * (dl / self.avgdl)))
                scores[chapter_id] += idf * tf_component

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return self._fetch_chapter_metadata([cid for cid, _ in ranked[:top_n]])

    def _fetch_chapter_metadata(self, chapter_ids):
        if not chapter_ids:
            return []

        placeholders = ",".join("?" for _ in chapter_ids)
        query = f"""
            SELECT chapter_id, book, chapter_title, text FROM chapters
            WHERE chapter_id IN ({placeholders})
        """
        return self.conn.execute(query, tuple(chapter_ids)).fetchall()

    def close(self):
        self.conn.close()