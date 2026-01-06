"""
RAG Chatbot - Knowledge Base Preparation
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Script to prepare and load knowledge base documents into the vector database
"""

import os
from pathlib import Path
from vector_store import VectorStoreManager
from langchain.schema import Document
try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
except ImportError:
    # Fallback for older LangChain versions
    from langchain.document_loaders import PyPDFLoader, TextLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_documents_from_directory(directory_path: str):
    """
    Load all documents from a directory.
    
    Args:
        directory_path: Path to the directory containing documents
        
    Returns:
        List of Document objects
    """
    documents = []
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Directory {directory_path} does not exist. Creating it...")
        directory.mkdir(parents=True, exist_ok=True)
        return documents
    
    # Supported file types
    supported_extensions = {'.pdf', '.txt', '.md'}
    
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                if file_path.suffix.lower() == '.pdf':
                    loader = PyPDFLoader(str(file_path))
                else:
                    loader = TextLoader(str(file_path))
                
                docs = loader.load()
                documents.extend(docs)
                print(f"Loaded {len(docs)} documents from {file_path.name}")
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
    
    return documents


def create_sample_knowledge_base():
    """
    Create a sample knowledge base with default content.
    """
    sample_documents = [
        Document(page_content="""
        RAG (Retrieval-Augmented Generation) is a technique that combines the power of 
        information retrieval with language generation. It works by first retrieving 
        relevant documents from a knowledge base, then using those documents as context 
        for generating accurate and informed responses.
        
        The main components of a RAG system include:
        1. A knowledge base containing documents
        2. A vector database for efficient similarity search
        3. An embedding model to convert text to vectors
        4. A language model for generating responses
        5. A retrieval mechanism to find relevant context
        """),
        Document(page_content="""
        Vector databases are specialized databases designed to store and query high-dimensional 
        vectors efficiently. They use techniques like approximate nearest neighbor search to 
        quickly find similar vectors.
        
        Popular vector databases include:
        - ChromaDB: Lightweight and easy to use
        - Pinecone: Managed vector database service
        - Weaviate: Open-source vector search engine
        - FAISS: Facebook's similarity search library
        
        Vector databases are essential for RAG systems as they enable fast retrieval of 
        relevant context from large knowledge bases.
        """),
        Document(page_content="""
        Embeddings are numerical representations of text that capture semantic meaning. 
        Similar texts have similar embeddings, which allows for semantic search.
        
        OpenAI provides several embedding models:
        - text-embedding-3-small: Fast and efficient
        - text-embedding-3-large: More accurate but slower
        - text-embedding-ada-002: Previous generation model
        
        Embeddings are created by neural networks trained on large text corpora. They 
        convert text into dense vectors that can be compared using cosine similarity.
        """),
        Document(page_content="""
        LangChain is a framework for building applications with large language models. 
        It provides abstractions for:
        - Document loaders and text splitters
        - Vector stores and retrievers
        - Chains for combining LLM calls
        - Agents for complex reasoning
        
        LangChain makes it easy to build RAG applications by providing pre-built components 
        that work together seamlessly. It supports multiple LLM providers including OpenAI, 
        Anthropic, and open-source models.
        """),
        Document(page_content="""
        Best practices for RAG systems:
        
        1. Chunk size: Use appropriate chunk sizes (typically 500-1000 tokens) to balance 
           context and precision
        
        2. Overlap: Include overlap between chunks to maintain context continuity
        
        3. Retrieval: Retrieve multiple relevant chunks (typically 3-5) to provide sufficient 
           context
        
        4. Prompting: Design clear prompts that instruct the LLM to use the provided context
        
        5. Evaluation: Regularly evaluate the system's performance and update the knowledge base
        
        6. Metadata: Store metadata with documents to enable filtering and better retrieval
        """)
    ]
    
    return sample_documents


def main():
    """
    Main function to prepare the knowledge base.
    """
    print("Initializing vector store...")
    vector_store = VectorStoreManager()
    
    # Check if knowledge base directory exists
    kb_directory = "./knowledge_base"
    
    if os.path.exists(kb_directory) and any(Path(kb_directory).iterdir()):
        print(f"Loading documents from {kb_directory}...")
        documents = load_documents_from_directory(kb_directory)
        
        if documents:
            print(f"Found {len(documents)} documents. Adding to vector store...")
            vector_store.add_documents(documents)
            print("Knowledge base prepared successfully!")
        else:
            print("No documents found. Creating sample knowledge base...")
            sample_docs = create_sample_knowledge_base()
            vector_store.add_documents(sample_docs)
            print("Sample knowledge base created successfully!")
    else:
        print("Knowledge base directory is empty. Creating sample knowledge base...")
        sample_docs = create_sample_knowledge_base()
        vector_store.add_documents(sample_docs)
        print("Sample knowledge base created successfully!")
    
    # Display collection info
    count = vector_store.get_collection_count()
    print(f"\nVector store contains {count} document chunks.")


if __name__ == "__main__":
    main()

