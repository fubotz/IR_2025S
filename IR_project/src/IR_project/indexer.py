from pathlib import Path
import sqlite3
from collections import Counter, defaultdict


class BooleanIndexerSQLite:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS inverted_index;")
            self.conn.execute("DROP TABLE IF EXISTS chapters;")
            self.conn.execute("DROP TABLE IF EXISTS vocabulary;")

            self.conn.execute("""
                CREATE TABLE inverted_index (
                    token TEXT,
                    chapter_id TEXT,
                    frequency INTEGER
                );
            """)
            self.conn.execute("CREATE INDEX idx_token ON inverted_index(token);")

            self.conn.execute("""
                CREATE TABLE chapters (
                    chapter_id TEXT PRIMARY KEY,
                    book TEXT,
                    chapter_title TEXT,
                    text TEXT
                );
            """)

            self.conn.execute("""
                CREATE TABLE vocabulary (
                    token TEXT PRIMARY KEY,
                    document_frequency INTEGER
                );
            """)

    def index_dataset(self, dataset):
        token_to_chapters = defaultdict(set)

        with self.conn:
            for entry in dataset:
                chapter_id = entry["chapter_id"]
                book = entry["book"]
                title = entry["chapter_title"]
                text = entry["text"]
                tokens = entry["tokens"]

                # Save chapter
                self.conn.execute("""
                    INSERT OR REPLACE INTO chapters (chapter_id, book, chapter_title, text)
                    VALUES (?, ?, ?, ?)
                """, (chapter_id, book, title, text))

                # Count token frequencies
                token_counts = Counter(tokens)
                for token, freq in token_counts.items():
                    token_to_chapters[token].add(chapter_id)
                    self.conn.execute("""
                        INSERT INTO inverted_index (token, chapter_id, frequency)
                        VALUES (?, ?, ?)
                    """, (token, chapter_id, freq))

            # Fill vocabulary table
            for token, chapters in token_to_chapters.items():
                self.conn.execute("""
                    INSERT INTO vocabulary (token, document_frequency)
                    VALUES (?, ?)
                """, (token, len(chapters)))

    def close(self):
        self.conn.close()






# class VectorIndexerSQLite:
#     def __init__(self, db_path):
#         self.db_path = Path(db_path)
#         self.conn = sqlite3.connect(self.db_path)
#         self._create_tables()
#