"""
RAG Chatbot - Configuration
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Configuration settings for the RAG chatbot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Configuration class for the RAG chatbot application.
    """
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    
    # Vector Database Configuration
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_db')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'knowledge_base')
    
    # Retrieval Configuration
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '5'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Knowledge Base Configuration
    KNOWLEDGE_BASE_PATH = os.getenv('KNOWLEDGE_BASE_PATH', './knowledge_base')
    
    @staticmethod
    def validate():
        """
        Validate that all required configuration is present.
        
        Returns:
            tuple: (is_valid, missing_keys)
        """
        required_keys = ['OPENAI_API_KEY']
        missing = []
        
        for key in required_keys:
            if not getattr(Config, key):
                missing.append(key)
        
        return len(missing) == 0, missing

