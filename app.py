"""
RAG Chatbot - Flask Application
Project: RAG Chatbot
Developer: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
Year: 2026
Description: Flask web application for the RAG chatbot
"""

from flask import Flask, render_template, request, jsonify, Response
from chatbot import RAGChatbot
from analytics import Analytics
from conversation_manager import ConversationManager
import os
import json
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = './knowledge_base'

# Initialize chatbot
try:
    chatbot = RAGChatbot()
    chatbot_initialized = True
except Exception as e:
    print(f"Error initializing chatbot: {str(e)}")
    chatbot = None
    chatbot_initialized = False

# Initialize analytics
analytics = Analytics()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'md', 'docx'}


@app.route('/')
def index():
    """
    Render the main chat interface.
    """
    return render_template('index.html')


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests with conversation history.
    """
    if not chatbot_initialized:
        return jsonify({
            "answer": "Chatbot is not initialized. Please check your configuration.",
            "sources": [],
            "success": False
        }), 500
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        use_hybrid = data.get('use_hybrid', False)
        include_history = data.get('include_history', True)
        
        if not question:
            return jsonify({
                "answer": "Please provide a question.",
                "sources": [],
                "success": False
            }), 400
        
        # Record session
        if session_id == 'default':
            session_id = str(uuid.uuid4())
            analytics.record_session()
        
        # Get response from chatbot
        response = chatbot.chat(question, session_id, use_hybrid, include_history)
        
        # Record analytics
        analytics.record_query(question, response.get('response_time'), response.get('sources', []))
        
        response['session_id'] = session_id
        return jsonify(response), 200
        
    except Exception as e:
        analytics.record_error()
        return jsonify({
            "answer": f"An error occurred: {str(e)}",
            "sources": [],
            "success": False
        }), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """
    Handle streaming chat requests.
    """
    if not chatbot_initialized:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not question:
            return jsonify({"error": "Please provide a question"}), 400
        
        def generate():
            for chunk in chatbot.stream_chat(question, session_id):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "healthy" if chatbot_initialized else "unhealthy",
        "initialized": chatbot_initialized
    }), 200


@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """
    Get conversation history for a session.
    """
    try:
        history = chatbot.conversation_manager.get_conversation_history(session_id)
        return jsonify({"history": history}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<session_id>', methods=['DELETE'])
def clear_conversation(session_id):
    """
    Clear conversation history for a session.
    """
    try:
        chatbot.conversation_manager.clear_conversation(session_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<session_id>/export', methods=['GET'])
def export_conversation(session_id):
    """
    Export conversation as JSON.
    """
    try:
        conversation_data = chatbot.conversation_manager.export_conversation(session_id)
        return jsonify(conversation_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """
    Upload and process a document to add to knowledge base.
    """
    if not chatbot_initialized:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process and add to knowledge base
            # Load the uploaded file
            try:
                from langchain_community.document_loaders import PyPDFLoader, TextLoader
            except ImportError:
                # Fallback for older LangChain versions
                from langchain.document_loaders import PyPDFLoader, TextLoader
            
            if filename.endswith('.pdf'):
                loader = PyPDFLoader(filepath)
            else:
                loader = TextLoader(filepath)
            
            documents = loader.load()
            chatbot.add_knowledge(documents)
            
            return jsonify({
                "success": True,
                "message": f"Document '{filename}' added to knowledge base",
                "chunks": len(documents)
            }), 200
        else:
            return jsonify({"error": "File type not allowed"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Get analytics and statistics.
    """
    try:
        days = request.args.get('days', 30, type=int)
        stats = analytics.get_stats(days)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback for a response.
    """
    try:
        data = request.get_json()
        positive = data.get('positive', True)
        analytics.record_feedback(positive)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/knowledge-base/stats', methods=['GET'])
def knowledge_base_stats():
    """
    Get knowledge base statistics.
    """
    if not chatbot_initialized:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        count = chatbot.vector_store_manager.get_collection_count()
        return jsonify({
            "document_count": count,
            "vector_db_path": chatbot.vector_store_manager.persist_directory
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

