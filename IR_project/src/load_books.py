import os
import re


def load_books_from_txt(folder_path):
    dataset = []

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        book_title = None
        current_chapter = None
        current_text = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            # Match book title like: "HP 1 - Harry Potter and the Sorcerer's Stone"
            if stripped.startswith("HP") and "Harry Potter" in stripped:
                book_title = stripped
                continue

            # Match chapters like: "CHAPTER ONE", "CHAPTER TWO", etc.
            if re.match(r"^CHAPTER\s+\w+", stripped, re.IGNORECASE):
                if current_chapter and current_text:
                    dataset.append({
                        "book": book_title,
                        "chapter": current_chapter,
                        "text": " ".join(current_text)
                    })
                    current_text = []
                current_chapter = stripped
                continue

            # Otherwise it's paragraph text
            current_text.append(stripped)

        # Add last chapter
        if current_chapter and current_text:
            dataset.append({
                "book": book_title,
                "chapter": current_chapter,
                "text": " ".join(current_text)
            })

    return dataset
