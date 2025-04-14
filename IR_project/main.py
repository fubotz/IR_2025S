from src.load_books import load_books_from_txt
from src.dataset_utils import save_to_json, save_to_jsonl, convert_to_hf_dataset

def main():
    dataset = load_books_from_txt("data/")

    print(f"Loaded {len(dataset)} chapters.\n")
    print("Example entry:", dataset[0])

    # Save to JSON and JSONL for easy reuse
    save_to_json(dataset, "data/harry_potter_dataset.json")
    save_to_jsonl(dataset, "data/harry_potter_dataset.jsonl")

    # Convert to Hugging Face dataset
    hf_dataset = convert_to_hf_dataset(dataset)
    print("\nHugging Face dataset preview:")
    print(hf_dataset[0])

if __name__ == "__main__":
    main()