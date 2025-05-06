import os

from IR_project.load_books import load_books_from_txt
from IR_project.dataset_utils import (
    save_to_json,
    save_to_jsonl,
    load_from_jsonl,
    convert_to_hf_datasets
)
from IR_project.preprocessing_dense import chunk_dataset_dense
from IR_project.preprocessing_BM25 import chunk_dataset_bm25


def main():
    dataset = None
    json_path = "../../data/processed/harry_potter_dataset.json"
    jsonl_path = "../../data/processed/harry_potter_dataset.jsonl"
    chunked_output_path_dense = "../../data/processed/hp_200w_chunks_dense.jsonl"
    chunked_output_path_bm25 = "../../data/processed/hp_200w_chunks_bm25.jsonl"

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

    # JSONL_chunked (BM25; sentence based)
    if not os.path.exists(chunked_output_path_bm25):
        if dataset is None:
            print("BM25 chunked JSONL not found — chunking and saving to JSONL.")
            dataset = load_from_jsonl(jsonl_path)
        chunked_dataset_bm25 = chunk_dataset_bm25(dataset, max_words=200)
        save_to_jsonl(chunked_dataset_bm25, chunked_output_path_bm25)
    else:
        print("BM25 chunked JSONL already exists, skipping chunking.")

    # JSONL_chunked (dense; 200 words, 50 overlap)
    if not os.path.exists(chunked_output_path_dense):
        if dataset is None:
            print("Chunked JSONL not found — chunking and saving to JSONL.")
            dataset = load_from_jsonl(jsonl_path)
        chunked_dataset = chunk_dataset_dense(dataset, chunk_size=200, overlap=50)
        save_to_jsonl(chunked_dataset, chunked_output_path_dense)
    else:
        print("Chunked JSONL already exists, skipping chunking.")


    # Load from existing JSONL
    dataset = load_from_jsonl(jsonl_path)
    chunked_dataset = chunk_dataset_dense(dataset, chunk_size=200, overlap=50)

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
