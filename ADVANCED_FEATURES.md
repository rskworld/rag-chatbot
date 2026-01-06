# Advanced Features Documentation

<!--
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
-->

## Overview

This document describes all the advanced features added to the RAG Chatbot.

## 1. Conversation History & Memory

The chatbot maintains conversation history across multiple messages, allowing for context-aware responses.

### Features:
- Session-based conversation tracking
- Automatic context inclusion in prompts
- Persistent storage of conversations
- Configurable history length

### Implementation:
- `ConversationManager` class manages all sessions
- Conversations stored in JSON format
- Last 5 messages included in context by default

## 2. Streaming Responses

Real-time streaming of LLM responses for better user experience.

### Features:
- Server-Sent Events (SSE) for streaming
- Real-time text display
- Smooth user experience
- Toggle on/off in UI

### Implementation:
- `/api/chat/stream` endpoint
- Event stream format
- Chunk-by-chunk response delivery

## 3. Hybrid Search

Combines vector similarity search with keyword matching for better results.

### Features:
- Weighted combination of vector and keyword scores
- Configurable weights (default: 70% vector, 30% keyword)
- Better handling of exact matches
- Improved relevance

### Implementation:
- `HybridSearch` class
- Jaccard similarity for keywords
- Normalized score combination
- Toggle in UI

## 4. File Upload

Upload documents directly through the web interface to add to knowledge base.

### Features:
- Drag and drop support
- Multiple file formats (PDF, TXT, MD)
- Automatic processing
- File size validation (16MB max)

### Implementation:
- `/api/upload` endpoint
- Automatic document loading and chunking
- Immediate availability after upload

## 5. Analytics & Statistics

Track usage, performance, and user feedback.

### Features:
- Query tracking
- Session statistics
- Response time monitoring
- Feedback collection
- Top queries and sources
- Time-based filtering

### Implementation:
- `Analytics` class
- Persistent storage in JSON
- Dashboard UI with charts
- `/api/analytics` endpoint

## 6. Feedback System

Users can provide feedback on responses.

### Features:
- Thumbs up/down buttons
- Feedback tracking
- Feedback score calculation
- Analytics integration

### Implementation:
- `/api/feedback` endpoint
- Stored in analytics
- Used for quality metrics

## 7. Chat Export

Export conversations for analysis or backup.

### Features:
- JSON format export
- Includes all messages and metadata
- Timestamp information
- Session-based export

### Implementation:
- `/api/conversation/<session_id>/export` endpoint
- Downloadable JSON file
- Complete conversation data

## 8. Session Management

Multiple concurrent sessions with independent history.

### Features:
- Unique session IDs
- Session-based conversation isolation
- Clear session functionality
- Session persistence

### Implementation:
- Automatic session ID generation
- Per-session conversation storage
- Session management endpoints

## 9. Advanced UI Features

Modern, responsive interface with advanced controls.

### Features:
- Modal dialogs
- Toggle switches
- File upload area
- Analytics dashboard
- Notification system
- Responsive design

### Implementation:
- Modern CSS with animations
- JavaScript event handling
- Mobile-friendly design

## API Endpoints

### Chat Endpoints
- `POST /api/chat` - Regular chat with conversation history
- `POST /api/chat/stream` - Streaming chat responses

### Conversation Endpoints
- `GET /api/conversation/<session_id>` - Get conversation history
- `DELETE /api/conversation/<session_id>` - Clear conversation
- `GET /api/conversation/<session_id>/export` - Export conversation

### Knowledge Base Endpoints
- `POST /api/upload` - Upload document to knowledge base
- `GET /api/knowledge-base/stats` - Get knowledge base statistics

### Analytics Endpoints
- `GET /api/analytics` - Get analytics and statistics
- `POST /api/feedback` - Submit feedback

### System Endpoints
- `GET /api/health` - Health check

## Configuration

All features can be configured via environment variables in `.env`:

```env
# Search Configuration
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Model Configuration
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo

# Hybrid Search Weights (in hybrid_search.py)
VECTOR_WEIGHT=0.7
KEYWORD_WEIGHT=0.3
```

## Performance Considerations

- Conversation history limited to last 50 messages per session
- Analytics data limited to last 10,000 entries
- Streaming reduces perceived latency
- Hybrid search slightly slower but more accurate
- File uploads processed asynchronously

## Future Enhancements

Potential features for future versions:
- Multi-language support
- Advanced chunking strategies
- Semantic chunking
- Metadata filtering
- Rate limiting
- User authentication
- Multi-tenant support
- Advanced analytics visualizations

## Support

For issues or questions:
- Website: https://rskworld.in
- Email: help@rskworld.in
- Phone: +91 93305 39277

© 2026 RSK World

