import os
import re

from word2number import w2n


def str_to_int(word):
    """Converts a string representation of a number to an integer."""
    try:
        return w2n.word_to_num(word.lower())
    except ValueError:
        return None


def load_books_from_txt(folder_path):
    """Loads books from a folder of .txt files and returns a formatted dataset."""
    dataset = []

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        book_title = None
        book_number = None
        current_chapter_str_num = None
        current_chapter_int_num = None
        current_chapter_title = None
        current_text = []

        lines_iter = iter(lines)
        for line in lines_iter:
            stripped = line.strip()

            if not stripped:
                continue

            # Match book titles like: "HP 1 - Harry Potter and the Sorcerer's Stone"
            if stripped.startswith("HP") and "Harry Potter" in stripped:
                book_title = stripped
                match = re.search(r"HP\s+(\d+)", stripped)
                if match:
                    book_number = int(match.group(1))
                continue

            # Match chapters like: "CHAPTER ONE"
            if re.match(r"^CHAPTER\s+\w+", stripped, re.IGNORECASE):
                # Save previous chapter before starting new one
                if current_chapter_str_num and current_text:
                    dataset.append({
                        "book": book_title,
                        "book_number": book_number,
                        "chapter_str_number": current_chapter_str_num,
                        "chapter_int_number": current_chapter_int_num,
                        "chapter_title": current_chapter_title,
                        "text": " ".join(current_text)
                    })
                    current_text = []

                current_chapter_str_num = stripped
                current_chapter_int_num = str_to_int(stripped.split()[-1])

                if current_chapter_int_num is None:
                    print(f"[WARNING] Could not convert chapter number: '{stripped.split()[-1]}'")
                    print(f"        Line: '{stripped}'")
                    print(f"        Book: '{book_title}', File: {filename}")

                # Next non-empty line = chapter title
                while True:
                    try:
                        next_line = next(lines_iter).strip()
                        if next_line:
                            current_chapter_title = next_line
                            break
                    except StopIteration:
                        current_chapter_title = ""
                        break
                continue

            # Regular paragraph
            current_text.append(stripped)

        # Save final chapter
        if current_chapter_str_num and current_text:
            dataset.append({
                "book": book_title,
                "book_number": book_number,
                "chapter_str_number": current_chapter_str_num,
                "chapter_int_number": current_chapter_int_num,
                "chapter_title": current_chapter_title,
                "text": " ".join(current_text)
            })

    return dataset



'''

mport logging
import re
from pathlib import Path
from word2number import w2n

logging.basicConfig(level=logging.WARNING)


def str_to_int(word):
    """Converts a string representation of a number to an integer."""
    try:
        return w2n.word_to_num(word.lower())
    except ValueError:
        return None


def parse_book_title(line):
    """Parses book title and number from a header line like 'HP 1 - ...'."""
    if line.startswith("HP") and "Harry Potter" in line:
        match = re.search(r"HP\s+(\d+)", line)
        book_number = int(match.group(1)) if match else None
        return line, book_number
    return None, None


def extract_chapter_title(lines_iter):
    """Extracts the next non-empty line as the chapter title."""
    for line in lines_iter:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def load_books_from_txt(folder_path):
    """Loads Harry Potter books from a folder of .txt files as structured chapter-level entries."""
    folder = Path(folder_path)

    for file_path in sorted(folder.glob("*.txt")):
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        book_title, book_number = None, None
        current_chapter_str_num = None
        current_chapter_int_num = None
        current_chapter_title = None
        current_text = []

        lines_iter = iter(lines)
        for line in lines_iter:
            stripped = line.strip()
            if not stripped:
                continue

            if not book_title:
                book_title, book_number = parse_book_title(stripped)
                if book_title:
                    continue

            # Match chapters like: CHAPTER ONE, CHAPTER TWELVE, etc.
            if re.fullmatch(r"CHAPTER\s+\w+", stripped, re.IGNORECASE):
                # Yield previous chapter
                if current_chapter_str_num and current_text:
                    yield {
                        "book": book_title,
                        "book_number": book_number,
                        "chapter_str_number": current_chapter_str_num,
                        "chapter_int_number": current_chapter_int_num,
                        "chapter_title": current_chapter_title,
                        "text": " ".join(" ".join(current_text).split()),
                        "chapter_id": f"{book_number:02d}_{current_chapter_int_num:02d}" if book_number and current_chapter_int_num else None
                    }
                    current_text = []

                current_chapter_str_num = stripped
                chapter_token = stripped.split()[-1]
                current_chapter_int_num = str_to_int(chapter_token)
                if current_chapter_int_num is None:
                    logging.warning(f"Could not convert chapter number: '{chapter_token}' in book '{book_title}' ({file_path.name})")

                current_chapter_title = extract_chapter_title(lines_iter)
                continue

            current_text.append(stripped)

        # Yield last chapter
        if current_chapter_str_num and current_text:
            yield {
                "book": book_title,
                "book_number": book_number,
                "chapter_str_number": current_chapter_str_num,
                "chapter_int_number": current_chapter_int_num,
                "chapter_title": current_chapter_title,
                "text": " ".join(" ".join(current_text).split()),
                "chapter_id": f"{book_number:02d}_{current_chapter_int_num:02d}" if book_number and current_chapter_int_num else None
            }

'''