from pathlib import Path


from IR_project.load_books import load_books_from_txt
from IR_project.dataset_utils import save_to_json, save_to_jsonl, convert_to_hf_dataset





def main():
    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[3]      # IR_2025S/

    # define paths
    raw_path = root_dir / "IR_project" / "data" / "raw"
    processed_path = root_dir / "IR_project" / "data" / "processed"

    json_path = processed_path / "dataset.json"
    jsonl_path = processed_path / "dataset.jsonl"

    # Load the chapters from raw .txt files
    dataset = list(load_books_from_txt(raw_path))
    print(f"✅ Loaded {len(dataset)} chapters from raw text.")

    # Save as JSON and JSONL
    save_to_json(dataset, json_path)
    save_to_jsonl(dataset, jsonl_path)
    print(f"📁 Saved JSON to: {json_path}")
    print(f"📁 Saved JSONL to: {jsonl_path}")

    # Optional: convert to HuggingFace Dataset
    hf_dataset = convert_to_hf_dataset(dataset)
    print(f"🤗 HuggingFace Dataset created with {hf_dataset.num_rows} rows.")
    print(hf_dataset[0])







if __name__ == "__main__":
    main()
