"""
RAG Chatbot - Embedding Utilities
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Handles text embeddings using OpenAI's embedding models
"""

import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmbeddingManager:
    """
    Manages text embeddings using OpenAI's embedding models.
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the embedding manager.
        
        Args:
            model_name: Name of the embedding model to use
        """
        self.model_name = model_name or os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.embeddings = OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=self.api_key
        )
    
    def embed_text(self, text: str):
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: list):
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
    
    def get_embeddings_instance(self):
        """
        Get the LangChain embeddings instance.
        
        Returns:
            OpenAIEmbeddings instance
        """
        return self.embeddings

