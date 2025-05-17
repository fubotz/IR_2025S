from pathlib import Path
from IR_2025S.dataset_utils import save_to_json, convert_to_hf_dataset, load_from_json
from IR_2025S.preprocessing import Preprocessor


def main():
    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[1]      # IR_2025S/
    processed_path = root_dir/"data"/"processed"
    json_path = processed_path/"dataset.json"
    preprocessed_path = processed_path/"dataset_preprocessed.json"

    dataset = load_from_json(json_path)
    print(f"📥 Loaded dataset from: {json_path}")

    preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
    dataset = preprocessor.preprocess_dataset(dataset)
    print(f"🧹 Preprocessed {len(dataset)} chapters.")

    save_to_json(dataset, preprocessed_path)
    print(f"📁 Saved preprocessed dataset to: {preprocessed_path}")

    # Optional: Convert to HF Dataset
    hf_dataset = convert_to_hf_dataset(dataset)
    print(f"🤗 HuggingFace Dataset created with {hf_dataset.num_rows} rows.")
    print(hf_dataset[0])


if __name__ == "__main__":
    main()
