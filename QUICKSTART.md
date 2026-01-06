# Quick Start Guide

<!--
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
-->

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or use the setup script:
   ```bash
   python setup.py
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Prepare knowledge base:**
   ```bash
   python prepare_knowledge_base.py
   ```
   This will create a sample knowledge base. You can add your own documents to the `knowledge_base/` directory.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:5000`

## Adding Your Own Knowledge Base

1. Place your documents (PDF, TXT, or MD files) in the `knowledge_base/` directory
2. Run `python prepare_knowledge_base.py` again
3. The documents will be processed and added to the vector database

## Troubleshooting

- **"OPENAI_API_KEY not found"**: Make sure you've created a `.env` file with your API key
- **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
- **Vector store errors**: Delete the `vector_db/` directory and run `prepare_knowledge_base.py` again

## Support

For issues or questions, contact:
- Website: https://rskworld.in
- Email: help@rskworld.in
- Phone: +91 93305 39277

© 2026 RSK World

