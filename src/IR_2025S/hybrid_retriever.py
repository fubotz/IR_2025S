from typing import List, Dict, Tuple
from collections import defaultdict
from IR_2025S.retriever import BM25RetrieverSQLite
from IR_2025S.dense_retriever import DenseRetrieverFAISS
from IR_2025S.preprocessing import Preprocessor

#
class HybridRetriever:
    """Combines BM25 sparse retrieval with dense retrieval using Reciprocal Rank Fusion."""

    def __init__(self,
                 bm25_db_path: str,
                 dense_index_path: str,
                 alpha: float = 0.5):  # alpha unused in RRF but kept for interface compatibility
        self.alpha = alpha
        self.bm25_retriever = BM25RetrieverSQLite(bm25_db_path)
        self.dense_retriever = DenseRetrieverFAISS()
        self.dense_retriever.load_index(dense_index_path)

    def search(self, query: str, query_tokens: List[str] = None, top_k: int = 5) -> List[Dict]:
        """Hybrid search combining BM25 and dense retrieval using RRF."""
        if query_tokens is None:
            preprocessor = Preprocessor(stopwords=True, lemmatize=True, preserve_punct=False)
            query_tokens = preprocessor.preprocess_text(query)

        bm25_results = self.bm25_retriever.rank_with_scores(query_tokens, top_n=top_k * 2)
        dense_results = self.dense_retriever.search(query, top_k=top_k * 2)

        combined_results = self._combine_results_rrf(bm25_results, dense_results, top_k=top_k, k=60)
        return combined_results

    def _combine_results_rrf(self,
                             bm25_results: List[Tuple[float, str, str, str, str]],
                             dense_results: List[Tuple[float, Dict]],
                             top_k: int = 5,
                             k: int = 60) -> List[Dict]:
        """Combine results using Reciprocal Rank Fusion and include match texts."""
        rrf_scores = defaultdict(float)

        # --- BM25 RRF scores ---
        for rank, (_, chapter_id, *_rest) in enumerate(bm25_results, start=1):
            rrf_scores[chapter_id] += 1 / (k + rank)

        # --- Dense RRF scores ---
        seen = set()
        dense_rank = 1
        for score, metadata in dense_results:
            chapter_id = metadata['chapter_id']
            if chapter_id not in seen:
                rrf_scores[chapter_id] += 1 / (k + dense_rank)
                seen.add(chapter_id)
                dense_rank += 1

        sorted_chapters = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        # --- Assembling enriched results ---
        results = []
        for chapter_id, combined_score in sorted_chapters[:top_k]:
            bm25_score = next((s for s, cid, *_ in bm25_results if cid == chapter_id), 0.0)
            dense_score = next((s for s, meta in dense_results if meta['chapter_id'] == chapter_id), 0.0)

            bm25_text = next((text for _, cid, _, _, text in bm25_results if cid == chapter_id), '')
            dense_text = next(
                (meta.get('paragraph_text', '') for _, meta in dense_results if meta['chapter_id'] == chapter_id), '')

            results.append({
                'chapter_id': chapter_id,
                'combined_score': combined_score,
                'bm25_score': bm25_score,
                'dense_score': dense_score,
                'bm25_text': bm25_text[:300].replace('\n', ' '),
                'dense_text': dense_text[:300].replace('\n', ' ')
            })

        return results

        # Assemble enriched results
        results = []
        for chapter_id, combined_score in sorted_chapters[:top_k]:
            bm25_score = next((s for s, cid, *_ in bm25_results if cid == chapter_id), 0.0)
            dense_score = next((s for s, meta in dense_results if meta['chapter_id'] == chapter_id), 0.0)
            paragraph_text = next((meta.get('paragraph_text', '') for _, meta in dense_results if meta['chapter_id'] == chapter_id), '')

            results.append({
                'chapter_id': chapter_id,
                'combined_score': combined_score,
                'bm25_score': bm25_score,
                'dense_score': dense_score,
                'paragraph_text': paragraph_text[:300].replace('\n', ' ')
            })

        return results

    def close(self):
        self.bm25_retriever.close()
