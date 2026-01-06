"""
RAG Chatbot - Vector Store Management
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Manages vector database operations using ChromaDB
"""

import os
import chromadb
from chromadb.config import Settings
try:
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
except ImportError:
    # Fallback for older LangChain versions
    from langchain.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
from embeddings import EmbeddingManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class VectorStoreManager:
    """
    Manages vector database operations for storing and retrieving documents.
    """
    
    def __init__(self, collection_name: str = None, persist_directory: str = None):
        """
        Initialize the vector store manager.
        
        Args:
            collection_name: Name of the collection in the vector database
            persist_directory: Directory to persist the vector database
        """
        self.collection_name = collection_name or os.getenv('COLLECTION_NAME', 'knowledge_base')
        self.persist_directory = persist_directory or os.getenv('VECTOR_DB_PATH', './vector_db')
        
        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager()
        
        # Initialize text splitter
        chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
        chunk_overlap = int(os.getenv('CHUNK_OVERLAP', '200'))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        # Initialize or load vector store
        self.vector_store = self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """
        Initialize or load the vector store from disk.
        
        Returns:
            Chroma vector store instance
        """
        try:
            # Try to load existing vector store
            vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_manager.get_embeddings_instance(),
                persist_directory=self.persist_directory
            )
            return vector_store
        except Exception:
            # Create new vector store if it doesn't exist
            vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_manager.get_embeddings_instance(),
                persist_directory=self.persist_directory
            )
            return vector_store
    
    def add_documents(self, documents: list):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects or text strings
        """
        # Convert strings to Document objects if needed
        if documents and isinstance(documents[0], str):
            documents = [Document(page_content=doc) for doc in documents]
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Add to vector store
        self.vector_store.add_documents(chunks)
        self.vector_store.persist()
    
    def add_texts(self, texts: list, metadatas: list = None):
        """
        Add texts directly to the vector store.
        
        Args:
            texts: List of text strings
            metadatas: Optional list of metadata dictionaries
        """
        # Split texts into chunks
        all_chunks = []
        all_metadatas = []
        
        for i, text in enumerate(texts):
            chunks = self.text_splitter.split_text(text)
            all_chunks.extend(chunks)
            if metadatas:
                for chunk in chunks:
                    all_metadatas.append(metadatas[i] if i < len(metadatas) else {})
        
        # Add to vector store
        if metadatas:
            self.vector_store.add_texts(texts=all_chunks, metadatas=all_metadatas)
        else:
            self.vector_store.add_texts(texts=all_chunks)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = None):
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        k = k or int(os.getenv('TOP_K_RESULTS', '5'))
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = None):
        """
        Search for similar documents with similarity scores.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (document, score)
        """
        k = k or int(os.getenv('TOP_K_RESULTS', '5'))
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def get_retriever(self, k: int = None):
        """
        Get a retriever instance for use with LangChain chains.
        
        Args:
            k: Number of results to return
            
        Returns:
            Vector store retriever
        """
        k = k or int(os.getenv('TOP_K_RESULTS', '5'))
        return self.vector_store.as_retriever(search_kwargs={"k": k})
    
    def delete_collection(self):
        """
        Delete the entire collection.
        """
        self.vector_store.delete_collection()
    
    def get_collection_count(self):
        """
        Get the number of documents in the collection.
        
        Returns:
            Number of documents
        """
        try:
            # Try to get count from collection
            if hasattr(self.vector_store, '_collection'):
                return self.vector_store._collection.count()
            # Alternative method
            elif hasattr(self.vector_store, 'collection'):
                return self.vector_store.collection.count()
            else:
                # Fallback: try to get all and count
                try:
                    results = self.vector_store.similarity_search("", k=10000)
                    return len(results)
                except:
                    return 0
        except Exception:
            return 0

