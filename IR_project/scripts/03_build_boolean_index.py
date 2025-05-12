from pathlib import Path
from IR_project.dataset_utils import load_from_json
from IR_project.indexer import BooleanIndexerSQLite


def main():
    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[2]      # IR_2025S/
    processed_path = root_dir/"IR_project"/"data"/"processed"
    dataset_path = processed_path/"dataset_preprocessed.json"
    db_path = processed_path/"boolean_index.db"

    # Load preprocessed dataset
    dataset = load_from_json(dataset_path)
    print(f"📥 Loaded {len(dataset)} chapters from: {dataset_path}")

    # Build SQLite index
    indexer = BooleanIndexerSQLite(db_path)
    indexer.index_dataset(dataset)
    indexer.close()
    print(f"✅ Boolean index created and saved to: {db_path}")


if __name__ == "__main__":
    main()



