# pipeline/06_query_dense.py#
#
import sys
from pathlib import Path

# Fix Python path to point to src/ folder where the IR_project module lives
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import argparse
from IR_2025S.dense_retriever import DenseRetrieverFAISS


def main():
    parser = argparse.ArgumentParser(description="Query Dense Retrieval Index")
    parser.add_argument("query", type=str, help="Search query (e.g. 'Harry talks to Dumbledore')")
    parser.add_argument("--topk", type=int, default=5, help="Number of results to return")
    parser.add_argument("--by-chapter", action="store_true", help="Group results by chapter")
    args = parser.parse_args()

    # project root = IR_2025S/
    root_dir = Path(__file__).resolve().parents[1]  # IR_2025S/
    processed_path = root_dir / "data" / "processed"
    dense_index_path = processed_path / "harry_dense_index"

    # Initialize and load dense retriever
    dense_retriever = DenseRetrieverFAISS()
    dense_retriever.load_index(str(dense_index_path))

    print(f"\n🔍 Dense Query: {args.query}  (Top {args.topk} results)\n")

    if args.by_chapter:
        # Search and group by chapter
        chapter_results = dense_retriever.search_by_chapter(args.query, top_k=args.topk)

        if not chapter_results:
            print("❌ No results found.")
            return

        for chapter_id, paragraphs in chapter_results.items():
            # Get chapter info from first paragraph
            first_para = paragraphs[0][1]
            print(f"📘 {first_para['book']} — {first_para['chapter_title']} ({chapter_id})")
            print(f"   Score: {paragraphs[0][0]:.4f}")

            for i, (score, metadata) in enumerate(paragraphs, 1):
                preview = metadata['paragraph_text'][:200].replace("\n", " ").strip() + "..."
                print(f"   {i}. [{score:.4f}] {preview}")
            print()

    else:
        # Regular paragraph-level search
        results = dense_retriever.search(args.query, top_k=args.topk)

        if not results:
            print("❌ No results found.")
            return

        for i, (score, metadata) in enumerate(results, 1):
            preview = metadata['paragraph_text'][:200].replace("\n", " ").strip() + "..."
            print(f"{i}. 📘 {metadata['book']} — {metadata['chapter_title']} ({metadata['chapter_id']})")
            print(f"   Score: {score:.4f}")
            print(f"   Paragraph {metadata['paragraph_idx']}: {preview}\n")


if __name__ == "__main__":
    main()


#run with
#python pipeline/07_dense_query.py "What is Hogwarts?" --topk 5