"""
RAG Chatbot - Analytics and Statistics
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Tracks analytics, statistics, and user feedback
"""

from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json
import os


class Analytics:
    """
    Tracks analytics and statistics for the chatbot.
    """
    
    def __init__(self):
        """
        Initialize analytics tracker.
        """
        self.storage_path = './analytics'
        self.data_file = os.path.join(self.storage_path, 'analytics.json')
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        
        # Load existing data
        self.data = self._load_data()
    
    def _load_data(self):
        """
        Load analytics data from disk.
        
        Returns:
            Dictionary with analytics data
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Return default structure
        return {
            'queries': [],
            'sessions': [],
            'feedback': [],
            'errors': [],
            'sources_used': []
        }
    
    def _save_data(self):
        """
        Save analytics data to disk.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    def record_query(self, query: str, response_time: float = None, sources: list = None):
        """
        Record a query.
        
        Args:
            query: User query
            response_time: Response time in seconds
            sources: List of sources used
        """
        query_record = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'response_time': response_time,
            'sources_count': len(sources) if sources else 0
        }
        
        self.data['queries'].append(query_record)
        
        # Record sources
        if sources:
            for source in sources:
                source_metadata = source.get('metadata', {})
                source_id = source_metadata.get('source', 'unknown')
                self.data['sources_used'].append({
                    'source': source_id,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Keep only last 10000 queries
        if len(self.data['queries']) > 10000:
            self.data['queries'] = self.data['queries'][-10000:]
        
        self._save_data()
    
    def record_session(self):
        """
        Record a new session.
        """
        session_record = {
            'timestamp': datetime.now().isoformat()
        }
        self.data['sessions'].append(session_record)
        
        # Keep only last 10000 sessions
        if len(self.data['sessions']) > 10000:
            self.data['sessions'] = self.data['sessions'][-10000:]
        
        self._save_data()
    
    def record_feedback(self, positive: bool):
        """
        Record user feedback.
        
        Args:
            positive: True for positive feedback, False for negative
        """
        feedback_record = {
            'positive': positive,
            'timestamp': datetime.now().isoformat()
        }
        self.data['feedback'].append(feedback_record)
        
        # Keep only last 10000 feedback entries
        if len(self.data['feedback']) > 10000:
            self.data['feedback'] = self.data['feedback'][-10000:]
        
        self._save_data()
    
    def record_error(self, error_type: str = 'unknown'):
        """
        Record an error.
        
        Args:
            error_type: Type of error
        """
        error_record = {
            'type': error_type,
            'timestamp': datetime.now().isoformat()
        }
        self.data['errors'].append(error_record)
        
        # Keep only last 1000 errors
        if len(self.data['errors']) > 1000:
            self.data['errors'] = self.data['errors'][-1000:]
        
        self._save_data()
    
    def get_stats(self, days: int = 30):
        """
        Get statistics for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()
        
        # Filter data by date
        recent_queries = [
            q for q in self.data['queries']
            if q['timestamp'] >= cutoff_iso
        ]
        
        recent_sessions = [
            s for s in self.data['sessions']
            if s['timestamp'] >= cutoff_iso
        ]
        
        recent_feedback = [
            f for f in self.data['feedback']
            if f['timestamp'] >= cutoff_iso
        ]
        
        recent_sources = [
            s for s in self.data['sources_used']
            if s['timestamp'] >= cutoff_iso
        ]
        
        # Calculate statistics
        total_queries = len(recent_queries)
        total_sessions = len(recent_sessions)
        
        # Average response time
        response_times = [q['response_time'] for q in recent_queries if q.get('response_time')]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Feedback score
        positive_feedback = sum(1 for f in recent_feedback if f['positive'])
        total_feedback = len(recent_feedback)
        feedback_score = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
        
        # Top queries
        query_texts = [q['query'] for q in recent_queries]
        top_queries = Counter(query_texts).most_common(10)
        
        # Top sources
        source_names = [s['source'] for s in recent_sources]
        top_sources = Counter(source_names).most_common(10)
        
        return {
            'total_queries': total_queries,
            'total_sessions': total_sessions,
            'avg_response_time': round(avg_response_time, 2),
            'feedback_score': round(feedback_score, 1),
            'total_feedback': total_feedback,
            'positive_feedback': positive_feedback,
            'top_queries': [{'query': q, 'count': c} for q, c in top_queries],
            'top_sources': [{'source': s, 'count': c} for s, c in top_sources],
            'period_days': days
        }
