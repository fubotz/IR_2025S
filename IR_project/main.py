import os

from src.load_books import load_books_from_txt
from src.dataset_utils import (
    save_to_json,
    save_to_jsonl,
    load_from_jsonl,
    convert_to_hf_dataset
)
from src.preprocessing import chunk_dataset


def main():
    dataset = None
    json_path = "data/processed/harry_potter_dataset.json"
    jsonl_path = "data/processed/harry_potter_dataset.jsonl"
    chunked_output_path = "data/processed/hp_chunks.jsonl"

    # JSON
    if not os.path.exists(json_path):
        print("JSON not found — loading from .txt and saving to JSON.")
        dataset = load_books_from_txt("data/raw/")
        save_to_json(dataset, json_path)
    else:
        print("JSON already exists, skipping save.")

    # JSONL
    if not os.path.exists(jsonl_path):
        if dataset is None:
            print("JSONL not found — loading from .txt and saving to JSONL.")
            dataset = load_books_from_txt("data/raw/")
        save_to_jsonl(dataset, jsonl_path)
    else:
        print("JSONL already exists, skipping save.")

    # JSONL_chunked
    if not os.path.exists(chunked_output_path):
        print("Chunked JSONL not found — chunking and saving to JSONL.")
        if dataset is None:
            dataset = load_from_jsonl(jsonl_path)
        chunked_dataset = chunk_dataset(dataset, chunk_size=200, overlap=50)
        save_to_jsonl(chunked_dataset, chunked_output_path)
    else:
        print("Chunked JSONL already exists, skipping chunking.")


    # Load from existing JSONL
    dataset = load_from_jsonl(jsonl_path)
    chunked_dataset = chunk_dataset(dataset, chunk_size=200, overlap=50)

    print(f"\nLoaded {len(dataset)} chapters.")
    print("Type:", type(dataset))

    print(f"\nLoaded {len(chunked_dataset)} chunks.")
    print("Type:", type(chunked_dataset))
    print("Example 0:", chunked_dataset[0])
    print("Example 1:", chunked_dataset[1])

    # # Convert to Hugging Face Dataset
    # hf_dataset = convert_to_hf_dataset(dataset)
    # print("HF Dataset Type:", type(hf_dataset))
    # print("Example:", hf_dataset[0])


if __name__ == "__main__":
    main()
