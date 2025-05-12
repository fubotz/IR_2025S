from pathlib import Path
import sqlite3


class BooleanIndexerSQLite:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()


    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS inverted_index (
                    token TEXT,
                    chapter_id TEXT
                );
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_token ON inverted_index(token);
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    chapter_id TEXT PRIMARY KEY,
                    book TEXT,
                    chapter_title TEXT,
                    text TEXT
                );
            """)


    def index_dataset(self, dataset):
        with self.conn:
            for entry in dataset:
                chapter_id = entry["chapter_id"]
                book = entry["book"]
                title = entry["chapter_title"]
                text = entry["text"]
                tokens = set(entry["tokens"])  # Avoid duplicate token inserts

                self.conn.execute("""
                    INSERT OR REPLACE INTO chapters (chapter_id, book, chapter_title, text)
                    VALUES (?, ?, ?, ?)
                """, (chapter_id, book, title, text))

                self.conn.executemany("""
                    INSERT INTO inverted_index (token, chapter_id)
                    VALUES (?, ?)
                """, [(token, chapter_id) for token in tokens])


    def search(self, query_tokens, operator="AND"):
        """
        Perform Boolean search on tokens using AND / OR.
        """
        if not query_tokens:
            return []

        with self.conn:
            results = []
            for token in query_tokens:
                rows = self.conn.execute("""
                    SELECT chapter_id FROM inverted_index WHERE token = ?
                """, (token.lower(),)).fetchall()
                results.append(set(r[0] for r in rows))

        if operator == "AND":
            matched_ids = set.intersection(*results)
        else:
            matched_ids = set.union(*results)

        return self._fetch_chapters(matched_ids)


    def _fetch_chapters(self, chapter_ids):
        if not chapter_ids:
            return []

        placeholders = ",".join("?" for _ in chapter_ids)
        query = f"SELECT chapter_id, book, chapter_title, text FROM chapters WHERE chapter_id IN ({placeholders})"
        with self.conn:
            return self.conn.execute(query, tuple(chapter_ids)).fetchall()


    def close(self):
        self.conn.close()
