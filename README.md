# RAG Chatbot

<!--
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Retrieval-Augmented Generation chatbot with knowledge base integration
-->

Retrieval-Augmented Generation chatbot with knowledge base integration. This chatbot uses RAG (Retrieval-Augmented Generation) architecture to provide accurate answers from a knowledge base. Perfect for building chatbots with domain-specific knowledge.

## Features

### Core Features
- Knowledge base integration with ChromaDB
- Vector similarity search
- Context retrieval from knowledge base
- Accurate responses using RAG architecture
- Domain-specific knowledge support

### Advanced Features
- **Conversation History**: Maintains context across multiple messages
- **Streaming Responses**: Real-time streaming of LLM responses
- **Hybrid Search**: Combines vector similarity with keyword matching
- **File Upload**: Upload documents directly through the web interface
- **Analytics Dashboard**: Track queries, sessions, response times, and feedback
- **Feedback System**: Thumbs up/down for responses
- **Chat Export**: Export conversations as JSON
- **Session Management**: Multiple concurrent sessions
- **Response Time Tracking**: Monitor performance metrics

## Technologies

- LangChain
- Vector DB (ChromaDB)
- Python
- OpenAI API
- Embeddings

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Prepare your knowledge base:
```bash
python prepare_knowledge_base.py
```

5. Run the application:
```bash
python app.py
```

## Usage

1. Start the Flask server
2. Open your browser and navigate to `http://localhost:5000`
3. Enter your questions in the chat interface
4. The chatbot will retrieve relevant context from the knowledge base and generate accurate responses

### Advanced Features Usage

- **Streaming Mode**: Toggle streaming on/off in the chat header
- **Hybrid Search**: Enable hybrid search for better results combining semantic and keyword search
- **Upload Documents**: Click the upload button to add new documents to the knowledge base
- **View Analytics**: Click the analytics button to see statistics and insights
- **Export Chat**: Click export to download your conversation as JSON
- **Feedback**: Use thumbs up/down buttons on responses to provide feedback

## Project Structure

```
rag-chatbot/
├── app.py                      # Flask application with advanced endpoints
├── chatbot.py                  # RAG chatbot implementation
├── vector_store.py             # Vector database operations
├── embeddings.py                # Embedding utilities
├── conversation_manager.py      # Conversation history management
├── analytics.py                # Analytics and statistics tracking
├── hybrid_search.py            # Hybrid search implementation
├── prepare_knowledge_base.py    # Knowledge base preparation
├── config.py                   # Configuration settings
├── setup.py                    # Setup script
├── templates/
│   └── index.html              # Web interface with advanced UI
├── static/
│   ├── css/
│   │   └── style.css           # Styles with modal and advanced UI
│   └── js/
│       └── app.js              # Frontend JavaScript with all features
├── knowledge_base/             # Knowledge base documents
├── vector_db/                  # Vector database storage
├── conversations/              # Conversation history storage
├── analytics/                  # Analytics data storage
└── requirements.txt            # Python dependencies
```

## License

© 2026 RSK World - https://rskworld.in

