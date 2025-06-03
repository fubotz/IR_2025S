import sys
from pathlib import Path

# Fix Python path to point to src/ folder where the IR_2025S module lives
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import argparse
from IR_2025S.preprocessing import Preprocessor
from IR_2025S.retriever import BM25RetrieverSQLite


def main():
    parser = argparse.ArgumentParser(description="Query BM25 index")
    parser.add_argument("query", type=str, help="Search query (e.g. 'harry dumbledore')")
    parser.add_argument("--topk", type=int, default=5, help="Number of results to return")
    args = parser.parse_args()

    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[1]      # IR_2025S/
    processed_path = root_dir/"data"/"processed"
    db_path = processed_path/"boolean_index.db"

    # preprocess query
    preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
    query_tokens = preprocessor.preprocess_text(args.query)

    if not query_tokens:
        print("❌ Query is empty after preprocessing.")
        return

    # run BM25 retrieval
    retriever = BM25RetrieverSQLite(db_path)
    results = retriever.rank(query_tokens, top_n=args.topk)
    retriever.close()

    # display results
    print(f"\n🔎 Query: {' '.join(query_tokens)}  (Top {args.topk} results)\n")
    if not results:
        print("❌ No results found.")
        return

    for i, (chapter_id, book, chapter_title, text) in enumerate(results, 1):
        preview = text[:300].replace("\n", " ").strip() + "..."
        print(f"{i}. 📘 {book} — {chapter_title} ({chapter_id})")
        print(f"   {preview}\n")


if __name__ == "__main__":
    main()

# in Terminal:
# conda activate IR_2025S
# python pipeline/04_query_bm25.py "dobby sock" --topk 5


#indexer next step
#retriever
#faiss embeddings
#query embeddings query hybrid (BM25 + dense retrieval)
#hybrid = reciprocal rank fusion
#ranking
#
# hi angi!

#####test