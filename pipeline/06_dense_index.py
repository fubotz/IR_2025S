# pipeline/0_6dense_index.py
#
import sys
from pathlib import Path

# Fix Python path to point to src/ folder where the IR_project module lives
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from IR_2025S.dataset_utils import load_from_json
from IR_2025S.dense_retriever import DenseRetrieverFAISS


def main():
    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[1]  # IR_2025S/
    processed_path = root_dir / "data" / "processed"
    dataset_path = processed_path / "dataset.json"  # Use original dataset, not preprocessed
    dense_index_path = processed_path / "dense_index"

    # Load dataset
    dataset = load_from_json(dataset_path)
    print(f"📥 Loaded {len(dataset)} chapters from: {dataset_path}")

    # Initialize dense retriever
    dense_retriever = DenseRetrieverFAISS()

    # Build dense index with paragraph-level embeddings
    print("🏗️ Building dense retrieval index...")
    dense_retriever.build_index(dataset, save_path=str(dense_index_path))

    print(f"✅ Dense index created and saved to: {dense_index_path}")


if __name__ == "__main__":
    main()
