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

    # Load from .txt and save if either file is missing
    if not os.path.exists(json_path) or not os.path.exists(jsonl_path):
        print("One or both JSON files missing — loading from .txt.")
        dataset = load_books_from_txt("data/")

        if not os.path.exists(json_path):
            save_to_json(dataset, json_path)
        else:
            print("JSON already exists, skipping save.")

        if not os.path.exists(jsonl_path):
            save_to_jsonl(dataset, jsonl_path)
        else:
            print("JSONL already exists, skipping save.")

    # Load from existing JSONL
    dataset = load_from_jsonl(jsonl_path)       # NB: jsonl better for hf dataset creation

    print(f"Loaded {len(dataset)} chapters.")
    print("Type:", type(dataset))

    # Convert to Hugging Face Dataset
    hf_dataset = convert_to_hf_dataset(dataset)
    print("Type:", type(hf_dataset))
    print("Example:", hf_dataset[0])


if __name__ == "__main__":
    main()
