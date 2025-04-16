import os

from src.load_books import load_books_from_txt
from src.dataset_utils import (
    save_to_json,
    save_to_jsonl,
    load_from_jsonl,
    convert_to_hf_dataset
)


def main():
    dataset = None
    json_path = "data/harry_potter_dataset.json"
    jsonl_path = "data/harry_potter_dataset.jsonl"

    # JSON
    if not os.path.exists(json_path):
        print("JSON not found — loading from .txt and saving to JSON.")
        dataset = load_books_from_txt("data/")
        save_to_json(dataset, json_path)
    else:
        print("JSON already exists, skipping save.")

    # JSONL
    if not os.path.exists(jsonl_path):
        if dataset is None:
            print("JSONL not found — loading from .txt and saving to JSONL.")
            dataset = load_books_from_txt("data/")
        save_to_jsonl(dataset, jsonl_path)
    else:
        print("JSONL already exists, skipping save.")

    # Load from existing JSONL
    dataset = load_from_jsonl(jsonl_path)

    print(f"\nLoaded {len(dataset)} chapters.")
    print("Type:", type(dataset))

    # Convert to Hugging Face Dataset
    hf_dataset = convert_to_hf_dataset(dataset)
    print("HF Dataset Type:", type(hf_dataset))
    print("Example:", hf_dataset[0])


if __name__ == "__main__":
    main()
