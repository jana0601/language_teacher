from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chat_handler import ChatHandler
from evaluator import LanguageEvaluator

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize handlers
chat_handler = ChatHandler()
evaluator = LanguageEvaluator()

# In-memory storage for sessions (can be upgraded to Redis later)
sessions = {}

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Return available languages for learning"""
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "ru", "name": "Russian"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "zh", "name": "Chinese"},
    ]
    return jsonify(languages)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and maintain conversation history"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        message = data.get('message')
        language = data.get('language')
        
        if not all([session_id, message, language]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Initialize session if it doesn't exist
        if session_id not in sessions:
            sessions[session_id] = {
                'language': language,
                'conversation': []
            }
        
        # Add user message to conversation
        sessions[session_id]['conversation'].append({
            'role': 'user',
            'content': message
        })
        
        # Get AI response
        ai_response = chat_handler.get_response(
            message, 
            language, 
            sessions[session_id]['conversation']
        )
        
        # Add AI response to conversation
        sessions[session_id]['conversation'].append({
            'role': 'assistant',
            'content': ai_response
        })
        
        return jsonify({
            "response": ai_response,
            "session_id": session_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Evaluate the conversation and return performance report"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id or session_id not in sessions:
            return jsonify({"error": "Invalid session ID"}), 400
        
        conversation = sessions[session_id]['conversation']
        language = sessions[session_id]['language']
        
        # Get evaluation report
        evaluation = evaluator.evaluate_conversation(conversation, language)
        
        return jsonify(evaluation)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/new', methods=['POST'])
def new_session():
    """Create a new conversation session"""
    import uuid
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'language': None,
        'conversation': []
    }
    return jsonify({"session_id": session_id})

@app.route('/api/session/<session_id>/clear', methods=['POST'])
def clear_session(session_id):
    """Clear conversation history for a session"""
    if session_id in sessions:
        sessions[session_id]['conversation'] = []
        return jsonify({"message": "Session cleared"})
    return jsonify({"error": "Session not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
