import faiss
import pickle
from pathlib import Path

# Path to the files
root = Path(__file__).resolve().parents[1]
index_path = root / "data" / "processed" / "harry_dense_index"

# Load FAISS index
faiss_index = faiss.read_index(str(index_path.with_suffix(".faiss")))

# Load metadata
with open(index_path.with_suffix(".pkl"), "rb") as f:
    metadata = pickle.load(f)

print(f"✅ Loaded index with {faiss_index.ntotal} vectors")
print(f"📄 First paragraph:\n{metadata[0]['paragraph_text']}")
#