# RAG Chatbot - Project Information

<!--
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
-->

## Project Overview

This is a complete RAG (Retrieval-Augmented Generation) chatbot implementation with knowledge base integration. The chatbot uses vector search to retrieve relevant context from a knowledge base and generates accurate, context-aware responses.

## Project Structure

```
rag-chatbot/
├── app.py                      # Flask web application
├── chatbot.py                  # RAG chatbot implementation
├── vector_store.py             # Vector database operations
├── embeddings.py               # Embedding utilities
├── config.py                   # Configuration settings
├── prepare_knowledge_base.py   # Knowledge base preparation script
├── setup.py                    # Setup/installation script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── QUICKSTART.md               # Quick start guide
├── LICENSE                     # MIT License
├── templates/
│   └── index.html              # Web interface template
├── static/
│   ├── css/
│   │   └── style.css           # Stylesheet
│   └── js/
│       └── app.js              # Frontend JavaScript
└── knowledge_base/
    └── sample_knowledge.txt    # Sample knowledge document
```

## Features Implemented

✅ Knowledge base integration with ChromaDB  
✅ Vector search and similarity matching  
✅ Context retrieval from knowledge base  
✅ Accurate responses using RAG architecture  
✅ Domain-specific knowledge support  
✅ Modern web interface  
✅ Real-time chat functionality  
✅ Source citation in responses  
✅ Responsive design  
✅ Error handling and validation  

## Technologies Used

- **LangChain**: Framework for LLM applications
- **ChromaDB**: Vector database for embeddings
- **OpenAI API**: For embeddings and LLM
- **Flask**: Web framework
- **Python**: Backend language
- **HTML/CSS/JavaScript**: Frontend

## Developer Information

All files in this project include developer information in comments:
- **Developer**: RSK World
- **Website**: https://rskworld.in
- **Email**: help@rskworld.in
- **Phone**: +91 93305 39277
- **Year**: 2026

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: Copy `.env.example` to `.env` and add your OpenAI API key
3. Prepare knowledge base: `python prepare_knowledge_base.py`
4. Run application: `python app.py`
5. Open browser: Navigate to `http://localhost:5000`

For detailed instructions, see `QUICKSTART.md` or `README.md`.

## License

MIT License - See LICENSE file for details.

© 2026 RSK World - https://rskworld.in

