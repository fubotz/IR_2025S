# src/IR_project/dense_retriever.py#
import torch
import faiss
import numpy as np
from pathlib import Path
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from typing import List, Tuple, Dict
import pickle
import re

#
class DenseRetrieverFAISS:
    def __init__(self,
                 index_path: str = None,
                 model_name: str = "facebook/dpr-ctx_encoder-single-nq-base",
                 question_model_name: str = "facebook/dpr-question_encoder-single-nq-base"):

        self.index_path = Path(index_path) if index_path else None
        self.model_name = model_name
        self.question_model_name = question_model_name

        # Disable gradients for inference
        torch.set_grad_enabled(False)

        # Load DPR models
        print("🤖 Loading DPR context encoder...")
        self.ctx_encoder = DPRContextEncoder.from_pretrained(model_name)
        self.ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(model_name)

        print("🤖 Loading DPR question encoder...")
        self.q_encoder = DPRQuestionEncoder.from_pretrained(question_model_name)
        self.q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(question_model_name)

        # Initialize FAISS index and metadata storage
        self.faiss_index = None
        self.paragraph_metadata = []  # Store paragraph info
        self.embedding_dim = 768  # DPR embedding dimension

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split chapter text into sentence-like paragraphs using end punctuation."""
        # Split on '.', '!' or '?' followed by space or newline and a capital letter (naive sentence boundary)
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“"])', text.strip())

        # Filter and clean
        paragraphs = [s.strip().replace('\n', ' ') for s in sentences if len(s.strip()) > 20]

        print(f"📄 Chapter has {len(paragraphs)} paragraphs.")
        return paragraphs


    def _encode_text(self, texts: List[str], batch_size: int = 16) -> np.ndarray:
        """Encode texts using DPR context encoder."""
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            # Tokenize batch
            inputs = self.ctx_tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )

            # Get embeddings
            with torch.no_grad():
                outputs = self.ctx_encoder(**inputs)
                batch_embeddings = outputs.pooler_output.numpy()
                embeddings.append(batch_embeddings)

        return np.vstack(embeddings)

    def build_index(self, dataset: List[Dict], save_path: str = None):
        """Build FAISS index from chapter dataset with paragraph-level embeddings."""
        print("📖 Processing chapters into paragraphs...")

        all_paragraphs = []
        paragraph_metadata = []

        for entry in dataset:
            chapter_id = entry["chapter_id"]
            book = entry["book"]
            chapter_title = entry["chapter_title"]
            text = entry["text"]

            # Split chapter into paragraphs
            paragraphs = self._split_into_paragraphs(text)

            for para_idx, paragraph in enumerate(paragraphs):
                all_paragraphs.append(paragraph)

                # Store metadata for each paragraph
                paragraph_metadata.append({
                    "chapter_id": chapter_id,
                    "book": book,
                    "chapter_title": chapter_title,
                    "paragraph_idx": para_idx,
                    "paragraph_text": paragraph,
                    "global_idx": len(paragraph_metadata)  # Global paragraph index
                })

        print(f"📝 Created {len(all_paragraphs)} paragraphs from {len(dataset)} chapters")

        # Encode all paragraphs
        print("🔢 Encoding paragraphs with DPR...")
        embeddings = self._encode_text(all_paragraphs)

        # Build FAISS index
        print("🏗️ Building FAISS index...")
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.faiss_index.add(embeddings)

        # Store metadata
        self.paragraph_metadata = paragraph_metadata

        print(f"✅ FAISS index built with {self.faiss_index.ntotal} vectors")

        # Save index and metadata if path provided
        if save_path:
            self.save_index(save_path)

    def save_index(self, save_path: str):
        """Save FAISS index and metadata to disk."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss_path = save_path.with_suffix('.faiss')
        faiss.write_index(self.faiss_index, str(faiss_path))

        # Save metadata
        metadata_path = save_path.with_suffix('.pkl')
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.paragraph_metadata, f)

        print(f"💾 Saved FAISS index to: {faiss_path}")
        print(f"💾 Saved metadata to: {metadata_path}")

    def load_index(self, load_path: str):
        """Load FAISS index and metadata from disk."""
        load_path = Path(load_path)

        # Load FAISS index
        faiss_path = load_path.with_suffix('.faiss')
        self.faiss_index = faiss.read_index(str(faiss_path))

        # Load metadata
        metadata_path = load_path.with_suffix('.pkl')
        with open(metadata_path, 'rb') as f:
            self.paragraph_metadata = pickle.load(f)

        print(f"📂 Loaded FAISS index from: {faiss_path}")
        print(f"📂 Loaded metadata from: {metadata_path}")

    def encode_query(self, query: str) -> np.ndarray:
        """Encode query using DPR question encoder."""
        inputs = self.q_tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.q_encoder(**inputs)
            query_embedding = outputs.pooler_output.numpy()

        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        return query_embedding

    def search(self, query: str, top_k: int = 5) -> List[Tuple[float, Dict]]:
        """Search for most relevant paragraphs."""
        if self.faiss_index is None:
            raise ValueError("Index not built or loaded. Call build_index() or load_index() first.")

        # Encode query
        query_embedding = self.encode_query(query)

        # Search FAISS index
        scores, indices = self.faiss_index.search(query_embedding, top_k)

        # Retrieve metadata for results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.paragraph_metadata):
                metadata = self.paragraph_metadata[idx].copy()
                results.append((float(score), metadata))

        return results

    def search_by_chapter(self, query: str, top_k: int = 5) -> Dict[str, List[Tuple[float, Dict]]]:
        """Search and group results by chapter."""
        results = self.search(query, top_k * 2)  # Get more results to group

        # Group by chapter
        chapter_results = {}
        for score, metadata in results:
            chapter_id = metadata['chapter_id']
            if chapter_id not in chapter_results:
                chapter_results[chapter_id] = []
            chapter_results[chapter_id].append((score, metadata))

        # Keep only top results per chapter and limit total
        final_results = {}
        count = 0
        for chapter_id, chapter_paragraphs in sorted(
                chapter_results.items(),
                key=lambda x: max(score for score, _ in x[1]),
                reverse=True
        ):
            if count >= top_k:
                break

            # Sort paragraphs in chapter by score
            chapter_paragraphs.sort(key=lambda x: x[0], reverse=True)
            final_results[chapter_id] = chapter_paragraphs[:3]  # Top 3 paragraphs per chapter
            count += 1

        return final_results
