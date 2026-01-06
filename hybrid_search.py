"""
RAG Chatbot - Hybrid Search
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Combines vector similarity search with keyword search
"""

import re
from collections import Counter


class HybridSearch:
    """
    Hybrid search combining vector similarity and keyword matching.
    """
    
    def __init__(self, vector_store_manager, vector_weight: float = 0.7, keyword_weight: float = 0.3):
        """
        Initialize hybrid search.
        
        Args:
            vector_store_manager: VectorStoreManager instance
            vector_weight: Weight for vector similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)
        """
        self.vector_store = vector_store_manager
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight
        
        # Normalize weights
        total_weight = vector_weight + keyword_weight
        if total_weight > 0:
            self.vector_weight /= total_weight
            self.keyword_weight /= total_weight
    
    def _extract_keywords(self, text: str):
        """
        Extract keywords from text.
        
        Args:
            text: Input text
            
        Returns:
            Set of keywords
        """
        # Convert to lowercase and split
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        return keywords
    
    def _keyword_score(self, query_keywords: set, document_text: str):
        """
        Calculate keyword matching score.
        
        Args:
            query_keywords: Set of query keywords
            document_text: Document text
            
        Returns:
            Keyword score (0-1)
        """
        if not query_keywords:
            return 0.0
        
        doc_keywords = self._extract_keywords(document_text)
        
        # Calculate Jaccard similarity
        intersection = len(query_keywords & doc_keywords)
        union = len(query_keywords | doc_keywords)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def search(self, query: str, k: int = 5):
        """
        Perform hybrid search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (document, combined_score)
        """
        # Get vector similarity results
        vector_results = self.vector_store.similarity_search_with_score(query, k=k * 2)
        
        # Extract keywords from query
        query_keywords = self._extract_keywords(query)
        
        # Calculate hybrid scores
        scored_results = []
        
        for doc, vector_score in vector_results:
            # Normalize vector score (assuming cosine similarity, -1 to 1)
            # Convert to 0-1 range
            normalized_vector_score = (vector_score + 1) / 2 if vector_score < 0 else 1 - (vector_score / 2)
            normalized_vector_score = max(0, min(1, normalized_vector_score))
            
            # Calculate keyword score
            keyword_score = self._keyword_score(query_keywords, doc.page_content)
            
            # Combine scores
            hybrid_score = (self.vector_weight * normalized_vector_score) + (self.keyword_weight * keyword_score)
            
            scored_results.append((doc, hybrid_score))
        
        # Sort by hybrid score (descending)
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        return scored_results[:k]
