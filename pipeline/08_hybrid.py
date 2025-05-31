# pipeline/08_hybrid.py
#
import sys
from pathlib import Path

# Add src/ to Python path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import argparse
from IR_2025S.preprocessing import Preprocessor
from IR_project.hybrid_retriever import HybridRetriever


def main():
    parser = argparse.ArgumentParser(description="Query Hybrid (BM25 + Dense) Retrieval")
    parser.add_argument("query", type=str, help="Search query (e.g. 'dobby house elf')")
    parser.add_argument("--topk", type=int, default=5, help="Number of results to return")
    parser.add_argument("--alpha", type=float, default=0.5, help="Weight for dense vs BM25 (0=BM25 only, 1=dense only)")
    args = parser.parse_args()

    # Define paths
    root_dir = Path(__file__).resolve().parents[1]  # IR_2025S/
    processed_path = root_dir / "data" / "processed"
    bm25_db_path = processed_path / "boolean_index.db"
    dense_index_path = processed_path / "harry_dense_index"

    # Initialize hybrid retriever
    hybrid_retriever = HybridRetriever(
        bm25_db_path=str(bm25_db_path),
        dense_index_path=str(dense_index_path),
        alpha=args.alpha
    )

    # Preprocess query
    preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
    query_tokens = preprocessor.preprocess_text(args.query)

    print(f"\n🔍 Hybrid Query: {args.query}")
    print(f"🔧 Processed tokens: {' '.join(query_tokens)}")
    print(f"⚖️ Alpha (dense weight): {args.alpha}")
    print(f"📊 Top {args.topk} results\n")

    # Run hybrid search
    results = hybrid_retriever.search(args.query, query_tokens=query_tokens, top_k=args.topk)

    if not results:
        print("❌ No results found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. Chapter {result['chapter_id']}")
            print(f"   🔗 Combined Score: {result['combined_score']:.4f}")
            print(f"   📚 BM25 Score: {result['bm25_score']:.4f}")
            print(f"   🤖 Dense Score: {result['dense_score']:.4f}")
            print(f"   📖 BM25 Snippet: {result['bm25_text']}")
            print(f"   🧠 Dense Snippet: {result['dense_text']}\n")

            bm25_text = result.get("bm25_text", "[No BM25 text available]")
            dense_text = result.get("dense_text", "[No dense text available]")

            print(f"   📖 BM25 Snippet: {bm25_text[:300].replace(chr(10), ' ')}...")
            print(f"   🧠 Dense Snippet: {dense_text[:300].replace(chr(10), ' ')}...\n")

    # Close DB connection
    hybrid_retriever.close()


print(f"HybridRetriever class loaded from: {HybridRetriever.__module__}")

if __name__ == "__main__":
    main()
