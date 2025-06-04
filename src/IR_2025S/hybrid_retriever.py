# Updated HybridRetriever using normalized score fusion (alpha-weighted) instead of RRF

from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict
from IR_2025S.retriever import BM25RetrieverSQLite
from IR_2025S.dense_retriever import DenseRetrieverFAISS
from IR_2025S.preprocessing import Preprocessor
from sklearn.preprocessing import MinMaxScaler

class HybridRetriever:


    def __init__(self,
                 bm25_db_path: str,
                 dense_index_path: str,
                 alpha: float = 0.5):
        self.alpha = alpha
        self.bm25_retriever = BM25RetrieverSQLite(bm25_db_path)
        self.dense_retriever = DenseRetrieverFAISS()
        self.dense_retriever.load_index(dense_index_path)

    def normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        if not scores:
            return {}
        keys = list(scores.keys())
        values = np.array(list(scores.values())).reshape(-1, 1)
        if len(values) > 1:
            normalized = MinMaxScaler().fit_transform(values).flatten()
        else:
            normalized = np.ones_like(values).flatten()
        return dict(zip(keys, normalized))

    def search(self, query: str, query_tokens: List[str] = None, top_k: int = 5) -> List[Dict]:
        if query_tokens is None:
            preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
            query_tokens = preprocessor.preprocess_text(query)

        # Retrieve from both retrievers
        bm25_results = self.bm25_retriever.rank_with_scores(query_tokens, top_n=top_k * 2)
        dense_results = self.dense_retriever.search(query, top_k=top_k * 2)

        # Extract and normalize scores
        bm25_scores = {cid: score for score, cid, *_ in bm25_results}
        dense_scores = {meta['chapter_id']: score for score, meta in dense_results}

        norm_bm25 = self.normalize_scores(bm25_scores)
        norm_dense = self.normalize_scores(dense_scores)

        # Combine scores using weighted sum
        combined_scores = defaultdict(float)
        all_doc_ids = set(norm_bm25.keys()).union(norm_dense.keys())
        for doc_id in all_doc_ids:
            combined_scores[doc_id] = (
                self.alpha * norm_dense.get(doc_id, 0.0) +
                (1 - self.alpha) * norm_bm25.get(doc_id, 0.0)
            )

        # Sort by combined score
        sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Assemble enriched results
        results = []
        for doc_id, combined_score in sorted_docs:
            bm25_score = bm25_scores.get(doc_id, 0.0)
            dense_score = dense_scores.get(doc_id, 0.0)

            bm25_text = next((text for _, cid, _, _, text in bm25_results if cid == doc_id), '')
            dense_text = next((meta.get('paragraph_text', '') for _, meta in dense_results if meta['chapter_id'] == doc_id), '')

            results.append({
                'chapter_id': doc_id,
                'combined_score': combined_score,
                'bm25_score': bm25_score,
                'dense_score': dense_score,
                'bm25_text': bm25_text[:300].replace('\\n', ' '),
                'dense_text': dense_text[:300].replace('\\n', ' ')
            })

        return results

    def close(self):
        self.bm25_retriever.close()



# python pipeline/08_hybrid.py "hogwarts school" --alpha 0.6 --topk 5
