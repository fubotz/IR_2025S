from pathlib import Path
from IR_2025S.load_books import load_books_from_txt
from IR_2025S.dataset_utils import save_to_json, save_to_jsonl


def main():
    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[1]      # IR_2025S/
    raw_path = root_dir/"data"/"raw"
    processed_path = root_dir/"data"/"processed"
    json_path = processed_path/"dataset.json"
    jsonl_path = processed_path/"dataset.jsonl"

    # load the chapters from raw .txt files
    dataset = list(load_books_from_txt(raw_path))
    print(f"✅ Loaded {len(dataset)} chapters from raw text.")

    # save as JSON and JSONL
    save_to_json(dataset, json_path)
    save_to_jsonl(dataset, jsonl_path)
    print(f"📁 Saved JSON to: {json_path}")
    print(f"📁 Saved JSONL to: {jsonl_path}")

# convert to HF Dataset here?

if __name__ == "__main__":
    main()