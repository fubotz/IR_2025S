# Update the 08_hybrid.py script to reflect new weighted hybrid behavior and keep argparse in __main__


# pipeline/08_hybrid.py

import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import argparse
from IR_2025S.preprocessing import Preprocessor
from IR_2025S.hybrid_retriever import HybridRetriever, DEFAULT_ALPHA

def run_hybrid_query(query: str, topk: int = 5, alpha: float = DEFAULT_ALPHA) -> List[dict]:
    root_dir = Path(__file__).resolve().parents[1]
    processed_path = root_dir / "data" / "processed"
    bm25_db_path = processed_path / "boolean_index.db"
    dense_index_path = processed_path / "harry_dense_index"

    hybrid_retriever = HybridRetriever(
        bm25_db_path=str(bm25_db_path),
        dense_index_path=str(dense_index_path),
        alpha=alpha
    )

    preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
    query_tokens = preprocessor.preprocess_text(query)

    results = hybrid_retriever.search(query, query_tokens=query_tokens, top_k=topk)
    hybrid_retriever.close()
    return results

def main():
    parser = argparse.ArgumentParser(description="Query Hybrid (BM25 + Dense) Retrieval with Weighted Fusion")
    parser.add_argument("query", type=str, help="Search query (e.g. 'dobby house elf')")
    parser.add_argument("--topk", type=int, default=5, help="Number of results to return")
    parser.add_argument("--alpha", type=float, default=DEFAULT_ALPHA, help="Weight for dense vs BM25 (0=BM25 only, 1=dense only)")
    args = parser.parse_args()

    results = run_hybrid_query(
        query=args.query,
        topk=args.topk,
        alpha=args.alpha
    )

    print(f"\n🔍 Hybrid Query: {args.query}")
    print(f"⚖️ Alpha (dense weight): {args.alpha}")
    print(f"📊 Top {args.topk} results\n")

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

if __name__ == "__main__":
    main()

#python pipeline/08_hybrid.py "harry potter godfather"
#python pipeline/08_hybrid.py "voldemort wand"