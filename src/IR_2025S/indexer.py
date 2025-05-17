import sqlite3
from pathlib import Path
from collections import Counter, defaultdict


# NB: implement phrase index? e.g. "harry potter" --> bigram?
# NB: implement positional index? e.g. "harry potter" --> [0, 1], [1, 2], [2, 3]...


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
                CREATE TABLE chapters (
                    chapter_id TEXT PRIMARY KEY,
                    book TEXT,
                    chapter_title TEXT,
                    text TEXT,
                    doc_length INTEGER
                );
            """)

            self.conn.execute("""
                CREATE TABLE inverted_index (
                    token TEXT,
                    chapter_id TEXT,
                    frequency INTEGER,
                    UNIQUE(token, chapter_id)
                );
            """)
            self.conn.execute("CREATE INDEX idx_token ON inverted_index(token);")

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
                doc_length = len(tokens)

                # chapter
                self.conn.execute("""
                    INSERT INTO chapters (chapter_id, book, chapter_title, text, doc_length)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(chapter_id) DO UPDATE SET
                        book = excluded.book,
                        chapter_title = excluded.chapter_title,
                        text = excluded.text,
                        doc_length = excluded.doc_length
                """, (chapter_id, book, title, text, doc_length))

                # index & frequencies
                token_counts = Counter(tokens)
                for token, freq in token_counts.items():
                    token_to_chapters[token].add(chapter_id)
                    self.conn.execute("""
                        INSERT INTO inverted_index (token, chapter_id, frequency)
                        VALUES (?, ?, ?)
                        ON CONFLICT(token, chapter_id) DO UPDATE SET
                            frequency = excluded.frequency
                    """, (token, chapter_id, freq))

            # vocabulary
            for token, chapters in token_to_chapters.items():
                # noinspection SqlResolve
                self.conn.execute("""
                    INSERT INTO vocabulary (token, document_frequency)
                    VALUES (?, ?)
                    ON CONFLICT(token) DO UPDATE SET
                        document_frequency = excluded.document_frequency
                """, (token, len(chapters)))

    def close(self):
        self.conn.close()






# class VectorIndexerSQLite:
#     def __init__(self, db_path):
#         self.db_path = Path(db_path)
#         self.conn = sqlite3.connect(self.db_path)
#         self._create_tables()
#