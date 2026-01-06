"""
RAG Chatbot - Conversation Manager
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Manages conversation history and context
"""

from collections import defaultdict
from datetime import datetime
import json
import os


class ConversationManager:
    """
    Manages conversation history for multiple sessions.
    """
    
    def __init__(self, max_history_per_session: int = 50):
        """
        Initialize the conversation manager.
        
        Args:
            max_history_per_session: Maximum number of messages to keep per session
        """
        self.conversations = defaultdict(list)
        self.max_history = max_history_per_session
        self.storage_path = './conversations'
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
    
    def add_message(self, session_id: str, role: str, content: str, metadata: dict = None):
        """
        Add a message to conversation history.
        
        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata dictionary
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.conversations[session_id].append(message)
        
        # Limit history size
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]
        
        # Persist to disk
        self._save_session(session_id)
    
    def get_conversation_history(self, session_id: str, limit: int = None):
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages to return
            
        Returns:
            List of message dictionaries
        """
        history = self.conversations.get(session_id, [])
        
        # Try to load from disk if not in memory
        if not history:
            history = self._load_session(session_id)
            if history:
                self.conversations[session_id] = history
        
        if limit:
            return history[-limit:]
        return history
    
    def get_context_messages(self, session_id: str, limit: int = 10):
        """
        Get recent messages formatted for context.
        
        Args:
            session_id: Session identifier
            limit: Number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        history = self.get_conversation_history(session_id)
        return history[-limit:] if history else []
    
    def clear_conversation(self, session_id: str):
        """
        Clear conversation history for a session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
        
        # Delete from disk
        file_path = os.path.join(self.storage_path, f"{session_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def export_conversation(self, session_id: str):
        """
        Export conversation as JSON.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with conversation data
        """
        history = self.get_conversation_history(session_id)
        return {
            'session_id': session_id,
            'exported_at': datetime.now().isoformat(),
            'message_count': len(history),
            'messages': history
        }
    
    def _save_session(self, session_id: str):
        """
        Save session to disk.
        
        Args:
            session_id: Session identifier
        """
        if session_id not in self.conversations:
            return
        
        file_path = os.path.join(self.storage_path, f"{session_id}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversations[session_id], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving session {session_id}: {e}")
    
    def _load_session(self, session_id: str):
        """
        Load session from disk.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of messages or None
        """
        file_path = os.path.join(self.storage_path, f"{session_id}.json")
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
    
    def get_all_sessions(self):
        """
        Get list of all session IDs.
        
        Returns:
            List of session IDs
        """
        sessions = set(self.conversations.keys())
        
        # Also check disk
        if os.path.exists(self.storage_path):
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    session_id = filename[:-5]  # Remove .json extension
                    sessions.add(session_id)
        
        return list(sessions)
