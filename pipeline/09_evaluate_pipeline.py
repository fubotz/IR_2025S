#  generate an evaluation script that:
# - Accepts a JSONL or JSON file with queries and relevant document IDs
# - Loops over alpha values
# - Runs the hybrid retriever
# - Computes MAP and NDCG

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import json
import argparse
from pathlib import Path
from collections import defaultdict
from sklearn.metrics import ndcg_score, average_precision_score
from IR_2025S.preprocessing import Preprocessor
from IR_2025S.hybrid_retriever import HybridRetriever


def load_dataset(path):
    with open(path, "r") as f:
        return json.load(f)


def get_relevant_texts(positive_ctxs):
    return set(ctx["text"].strip() for ctx in positive_ctxs if "text" in ctx)


def evaluate_query(retriever, query, relevant_texts, topk):
    preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
    query_tokens = preprocessor.preprocess_text(query)
    results = retriever.search(query, query_tokens=query_tokens, top_k=topk)

    y_true = []
    y_scores = []

    for r in results:
        bm25_text = r.get("bm25_text", "")
        dense_text = r.get("dense_text", "")

        is_relevant = any(
            rel_text.lower() in bm25_text.lower() or rel_text.lower() in dense_text.lower()
            for rel_text in relevant_texts
        )

        y_true.append(1 if is_relevant else 0)
        y_scores.append(r["combined_score"])

    ap = average_precision_score(y_true, y_scores) if any(y_true) else 0.0
    ndcg = ndcg_score([y_true], [y_scores]) if any(y_true) else 0.0
    return ap, ndcg


def evaluate_all(data_path, bm25_path, dense_path, topk=5):
    dataset = load_dataset(data_path)
    alpha_results = defaultdict(list)

    for alpha in [x / 10.0 for x in range(0, 11)]:
        print(f"🔁 Evaluating for alpha = {alpha:.1f}")
        retriever = HybridRetriever(bm25_db_path=bm25_path, dense_index_path=dense_path, alpha=alpha)
        total_ap, total_ndcg = 0.0, 0.0

        for entry in dataset:
            query = entry["query"]
            relevant_texts = get_relevant_texts(entry.get("positive_ctxs", []))
            ap, ndcg = evaluate_query(retriever, query, relevant_texts, topk)
            total_ap += ap
            total_ndcg += ndcg

        retriever.close()
        avg_ap = total_ap / len(dataset)
        avg_ndcg = total_ndcg / len(dataset)
        alpha_results["alpha"].append(alpha)
        alpha_results["MAP"].append(avg_ap)
        alpha_results["NDCG"].append(avg_ndcg)
        print(f"✅ Alpha: {alpha:.1f} | MAP: {avg_ap:.4f} | NDCG: {avg_ndcg:.4f}")

    return alpha_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Path to evaluation JSON file")
    parser.add_argument("--topk", type=int, default=5)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    processed = root / "data" / "processed"
    bm25 = processed / "boolean_index.db"
    dense = processed / "harry_dense_index"

    evaluate_all(args.data, str(bm25), str(dense), topk=args.topk)


if __name__ == "__main__":
    main()


#python pipeline/09_evaluate_pipeline.py data/processed/eval_data.json --topk 5

