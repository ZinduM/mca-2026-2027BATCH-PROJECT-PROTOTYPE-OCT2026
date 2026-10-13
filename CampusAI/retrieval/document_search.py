"""
CampusAI - Document Search Engine
Implements TF-IDF, BM25 ranking, passage retrieval, and semantic search
for college documents (syllabi, rules, policies, etc.)
"""

import re
import math
import os
import sys
from collections import Counter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from backend.database import execute_raw_sql


class DocumentSearchEngine:
    """
    Information Retrieval engine for college documents.
    Supports TF-IDF vectorization, BM25 ranking, and passage retrieval.
    """

    def __init__(self):
        self.documents = []
        self.doc_index = {}
        self.idf_cache = {}
        self.avg_doc_length = 0
        self._load_documents()

    def _load_documents(self):
        """Load documents from the database."""
        result = execute_raw_sql("SELECT document_id, title, category, content FROM documents")
        if result["success"] and result["data"]:
            self.documents = result["data"]
            self._build_index()

    def _build_index(self):
        """Build inverted index and compute IDF values."""
        total_length = 0
        doc_freq = Counter()

        for doc in self.documents:
            tokens = self._tokenize(doc["content"])
            total_length += len(tokens)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] += 1

            self.doc_index[doc["document_id"]] = {
                "tokens": tokens,
                "tf": Counter(tokens),
                "length": len(tokens),
                "title": doc["title"],
                "category": doc["category"],
                "content": doc["content"]
            }

        n = len(self.documents)
        self.avg_doc_length = total_length / max(n, 1)

        # Compute IDF for all terms
        for term, df in doc_freq.items():
            self.idf_cache[term] = math.log((n - df + 0.5) / (df + 0.5) + 1)

    def _tokenize(self, text):
        """Tokenize text into lowercase words, removing stopwords."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "need", "dare", "ought",
            "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "above", "below",
            "between", "out", "off", "over", "under", "again", "further", "then",
            "once", "here", "there", "when", "where", "why", "how", "all", "each",
            "every", "both", "few", "more", "most", "other", "some", "such", "no",
            "not", "only", "own", "same", "so", "than", "too", "very", "just",
            "because", "but", "and", "or", "if", "while", "this", "that", "these",
            "those", "it", "its", "i", "me", "my", "we", "our", "you", "your",
            "he", "him", "his", "she", "her", "they", "them", "their", "what",
            "which", "who", "whom"
        }
        words = re.findall(r'\b[a-z]+\b', text.lower())
        return [w for w in words if w not in stopwords and len(w) > 1]

    # ── TF-IDF Search ──────────────────────────────────────────────────────

    def tfidf_search(self, query, top_k=5):
        """
        Search documents using TF-IDF scoring.
        TF-IDF(t,d) = TF(t,d) × IDF(t)
        """
        query_tokens = self._tokenize(query)
        scores = []

        for doc_id, doc_info in self.doc_index.items():
            score = 0
            for token in query_tokens:
                tf = doc_info["tf"].get(token, 0) / max(doc_info["length"], 1)
                idf = self.idf_cache.get(token, 0)
                score += tf * idf
            if score > 0:
                scores.append({
                    "document_id": doc_id,
                    "title": doc_info["title"],
                    "category": doc_info["category"],
                    "score": round(score, 4),
                    "method": "TF-IDF"
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    # ── BM25 Search ────────────────────────────────────────────────────────

    def bm25_search(self, query, top_k=5, k1=1.5, b=0.75):
        """
        Search documents using BM25 ranking algorithm.
        BM25 is an improved TF-IDF that accounts for document length normalization.

        BM25(D,Q) = Σ IDF(qi) × (f(qi,D) × (k1 + 1)) / (f(qi,D) + k1 × (1 - b + b × |D|/avgdl))
        """
        query_tokens = self._tokenize(query)
        scores = []

        for doc_id, doc_info in self.doc_index.items():
            score = 0
            doc_len = doc_info["length"]

            for token in query_tokens:
                tf = doc_info["tf"].get(token, 0)
                idf = self.idf_cache.get(token, 0)

                # BM25 formula
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_len / max(self.avg_doc_length, 1)))
                score += idf * (numerator / max(denominator, 0.001))

            if score > 0:
                scores.append({
                    "document_id": doc_id,
                    "title": doc_info["title"],
                    "category": doc_info["category"],
                    "score": round(score, 4),
                    "method": "BM25"
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    # ── Passage Retrieval ──────────────────────────────────────────────────

    def passage_retrieval(self, query, top_k=3, window_size=3):
        """
        Retrieve the most relevant passages from documents.
        Splits documents into sentence-level passages and ranks them.
        """
        query_tokens = set(self._tokenize(query))
        passages = []

        for doc_id, doc_info in self.doc_index.items():
            content = doc_info["content"]
            sentences = re.split(r'[.!?]+', content)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

            # Create sliding window passages
            for i in range(len(sentences)):
                end = min(i + window_size, len(sentences))
                passage = ". ".join(sentences[i:end])
                passage_tokens = set(self._tokenize(passage))

                # Score based on overlap with query
                overlap = len(query_tokens & passage_tokens)
                if overlap > 0:
                    score = overlap / max(len(query_tokens), 1)
                    # Boost score for exact phrase matches
                    query_lower = query.lower()
                    if any(qt in passage.lower() for qt in query.lower().split()):
                        score *= 1.2

                    passages.append({
                        "document_id": doc_id,
                        "title": doc_info["title"],
                        "category": doc_info["category"],
                        "passage": passage[:500],  # Limit passage length
                        "score": round(score, 4),
                        "method": "Passage Retrieval"
                    })

        passages.sort(key=lambda x: x["score"], reverse=True)
        return passages[:top_k]

    # ── Semantic Search ────────────────────────────────────────────────────

    def semantic_search(self, query, top_k=5):
        """
        Semantic search using cosine similarity on TF-IDF vectors.
        Computes cosine similarity between query vector and document vectors.
        """
        query_tokens = self._tokenize(query)
        query_tf = Counter(query_tokens)

        # Build query vector
        query_vec = {}
        for token in query_tokens:
            tf = query_tf[token] / max(len(query_tokens), 1)
            idf = self.idf_cache.get(token, 0)
            query_vec[token] = tf * idf

        query_norm = math.sqrt(sum(v ** 2 for v in query_vec.values()))
        if query_norm == 0:
            return []

        scores = []
        for doc_id, doc_info in self.doc_index.items():
            # Build document vector
            doc_vec = {}
            for token, count in doc_info["tf"].items():
                tf = count / max(doc_info["length"], 1)
                idf = self.idf_cache.get(token, 0)
                doc_vec[token] = tf * idf

            doc_norm = math.sqrt(sum(v ** 2 for v in doc_vec.values()))
            if doc_norm == 0:
                continue

            # Cosine similarity
            dot_product = sum(query_vec.get(t, 0) * doc_vec.get(t, 0)
                              for t in set(query_vec) | set(doc_vec))
            similarity = dot_product / (query_norm * doc_norm)

            if similarity > 0:
                scores.append({
                    "document_id": doc_id,
                    "title": doc_info["title"],
                    "category": doc_info["category"],
                    "score": round(similarity, 4),
                    "method": "Semantic (Cosine)"
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    # ── Combined Search ────────────────────────────────────────────────────

    def search(self, query, top_k=5):
        """
        Combined search using multiple retrieval methods.
        Merges results from TF-IDF, BM25, passage retrieval, and semantic search.
        Returns ranked results with retrieved passages.
        """
        tfidf_results = self.tfidf_search(query, top_k)
        bm25_results = self.bm25_search(query, top_k)
        passages = self.passage_retrieval(query, top_k)
        semantic_results = self.semantic_search(query, top_k)

        # Merge and deduplicate by document_id
        seen = set()
        merged = []

        # Weight: BM25 > Semantic > TF-IDF
        for result in bm25_results + semantic_results + tfidf_results:
            doc_id = result["document_id"]
            if doc_id not in seen:
                seen.add(doc_id)
                # Find the matching passage for this document
                doc_passage = next(
                    (p for p in passages if p["document_id"] == doc_id),
                    None
                )
                result["passage"] = doc_passage["passage"] if doc_passage else ""
                merged.append(result)

        return {
            "query": query,
            "results": merged[:top_k],
            "total_documents_searched": len(self.documents),
            "retrieval_methods": ["TF-IDF", "BM25", "Passage Retrieval", "Semantic (Cosine)"]
        }

    def refresh(self):
        """Reload documents from database and rebuild index."""
        self.documents = []
        self.doc_index = {}
        self.idf_cache = {}
        self._load_documents()


# ── Singleton Instance ─────────────────────────────────────────────────────────

search_engine = DocumentSearchEngine()
