"""
RAG Chatbot - Main Chatbot Implementation
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: RAG (Retrieval-Augmented Generation) chatbot implementation
"""

import os
import time
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vector_store import VectorStoreManager
from hybrid_search import HybridSearch
from conversation_manager import ConversationManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RAGChatbot:
    """
    RAG Chatbot that combines retrieval from knowledge base with LLM generation.
    """
    
    def __init__(self):
        """
        Initialize the RAG chatbot.
        """
        # Initialize vector store manager
        self.vector_store_manager = VectorStoreManager()
        
        # Initialize hybrid search
        self.hybrid_search = HybridSearch(self.vector_store_manager)
        
        # Initialize conversation manager
        self.conversation_manager = ConversationManager()
        
        # Initialize LLM
        model_name = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            openai_api_key=api_key,
            streaming=True
        )
        
        # Create custom prompt template with conversation history support
        self.prompt_template = PromptTemplate(
            template="""You are a helpful AI assistant that answers questions based on the provided context and conversation history.

Previous conversation:
{chat_history}

Context information:
{context}

Question: {question}

Please provide a detailed and accurate answer based on the context above. If the context doesn't contain enough information to answer the question, say so and provide a general answer if possible. Use the conversation history to maintain context and provide coherent responses.

Answer:""",
            input_variables=["context", "question", "chat_history"]
        )
        
        # Initialize QA chain
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self, use_hybrid: bool = False):
        """
        Create the RetrievalQA chain.
        
        Args:
            use_hybrid: Whether to use hybrid search
        
        Returns:
            RetrievalQA chain instance
        """
        if use_hybrid:
            # Custom retriever using hybrid search
            class HybridRetriever:
                def __init__(self, hybrid_search):
                    self.hybrid_search = hybrid_search
                
                def get_relevant_documents(self, query):
                    results = self.hybrid_search.search(query, k=5)
                    return [doc for doc, _ in results]
            
            retriever = HybridRetriever(self.hybrid_search)
        else:
            retriever = self.vector_store_manager.get_retriever()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        return qa_chain
    
    def chat(self, question: str, session_id: str = "default", use_hybrid: bool = False, include_history: bool = True):
        """
        Process a user question and return a response.
        
        Args:
            question: User's question
            session_id: Session identifier for conversation history
            use_hybrid: Whether to use hybrid search
            include_history: Whether to include conversation history
            
        Returns:
            Dictionary with 'answer' and 'sources'
        """
        start_time = time.time()
        
        try:
            # Get conversation history if enabled
            chat_history = ""
            if include_history:
                history_messages = self.conversation_manager.get_context_messages(session_id)
                if history_messages:
                    # Format history for prompt
                    history_text = "\n".join([
                        f"{msg['role']}: {msg['content']}"
                        for msg in history_messages[-5:]  # Last 5 messages
                    ])
                    chat_history = history_text
            
            # Create chain with history if needed
            if include_history and chat_history:
                qa_chain = self._create_qa_chain_with_history(use_hybrid)
                result = qa_chain({"query": question, "chat_history": chat_history})
            else:
                if use_hybrid:
                    qa_chain = self._create_qa_chain(use_hybrid=True)
                else:
                    qa_chain = self.qa_chain
                result = qa_chain({"query": question})
            
            # Extract answer and sources
            answer = result.get("result", "I'm sorry, I couldn't generate a response.")
            source_documents = result.get("source_documents", [])
            
            # Format sources
            sources = []
            for doc in source_documents:
                sources.append({
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                })
            
            # Record in conversation history
            if include_history:
                self.conversation_manager.add_message(session_id, "user", question)
                self.conversation_manager.add_message(session_id, "assistant", answer, {"sources": sources})
            
            response_time = time.time() - start_time
            
            return {
                "answer": answer,
                "sources": sources,
                "success": True,
                "response_time": round(response_time, 2)
            }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "answer": f"I encountered an error: {str(e)}",
                "sources": [],
                "success": False,
                "response_time": round(response_time, 2)
            }
    
    def _create_qa_chain_with_history(self, use_hybrid: bool = False):
        """
        Create QA chain with conversation history support.
        
        Args:
            use_hybrid: Whether to use hybrid search
            
        Returns:
            RetrievalQA chain instance
        """
        if use_hybrid:
            class HybridRetriever:
                def __init__(self, hybrid_search):
                    self.hybrid_search = hybrid_search
                
                def get_relevant_documents(self, query):
                    results = self.hybrid_search.search(query, k=5)
                    return [doc for doc, _ in results]
            
            retriever = HybridRetriever(self.hybrid_search)
        else:
            retriever = self.vector_store_manager.get_retriever()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        return qa_chain
    
    def get_context(self, question: str, k: int = 5):
        """
        Get relevant context for a question without generating a response.
        
        Args:
            question: User's question
            k: Number of context chunks to retrieve
            
        Returns:
            List of relevant document chunks
        """
        return self.vector_store_manager.similarity_search(question, k=k)
    
    def add_knowledge(self, documents: list):
        """
        Add new documents to the knowledge base.
        
        Args:
            documents: List of Document objects or text strings
        """
        self.vector_store_manager.add_documents(documents)
        # Recreate QA chain to include new documents
        self.qa_chain = self._create_qa_chain()
    
    def stream_chat(self, question: str, session_id: str = "default"):
        """
        Stream chat response in real-time.
        
        Args:
            question: User's question
            session_id: Session identifier
            
        Yields:
            Chunks of the response
        """
        try:
            # Get context
            retriever = self.vector_store_manager.get_retriever()
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Get conversation history
            history_messages = self.conversation_manager.get_context_messages(session_id)
            chat_history = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in history_messages[-5:]
            ]) if history_messages else ""
            
            # Create prompt
            prompt = self.prompt_template.format(
                context=context,
                question=question,
                chat_history=chat_history if chat_history else "No previous conversation."
            )
            
            # Stream response
            full_response = ""
            for chunk in self.llm.stream(prompt):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    full_response += content
                    yield content
                elif isinstance(chunk, str) and chunk:
                    full_response += chunk
                    yield chunk
                elif hasattr(chunk, 'choices') and chunk.choices:
                    # Handle OpenAI API response format
                    for choice in chunk.choices:
                        if hasattr(choice, 'delta') and hasattr(choice.delta, 'content') and choice.delta.content:
                            content = choice.delta.content
                            full_response += content
                            yield content
            
            # Record in history
            self.conversation_manager.add_message(session_id, "user", question)
            self.conversation_manager.add_message(session_id, "assistant", full_response)
            
        except Exception as e:
            yield f"Error: {str(e)}"

