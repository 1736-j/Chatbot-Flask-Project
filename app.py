from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import requests  # To make HTTP requests to Rasa server
from config import Config
from model import db, Assistant, Prompt, ChatbotConversion

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS and database
CORS(app)
db.init_app(app)

# Rasa server configuration
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"  # Adjust if Rasa runs on a different URL/port

@app.route('/')
def index():
    return "Welcome to the Sensia Project API!"

# API to get all assistants
@app.route('/api/assistants', methods=['GET'])
def get_assistants():
    assistants = Assistant.query.all()
    result = [
        {'id': a.id, 'name': a.name, 'image_url': a.image_url, 'status': a.status}
        for a in assistants
    ]
    return jsonify(result)

# Route to create a new agent (assistant)
@app.route("/api/assistants", methods=["POST"])
def create_assistant():
    try:
        data = request.json
        name = data.get("name")
        image_url = data.get("image_url", "")  # Default to empty string if not provided
        
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Create a new assistant instance
        new_assistant = Assistant(name=name, image_url=image_url)
        db.session.add(new_assistant)
        db.session.commit()

        return jsonify({
            "message": "Assistant created successfully",
            "assistant": {
                "id": new_assistant.id,
                "name": new_assistant.name,
                "image_url": new_assistant.image_url,
                "status": new_assistant.status,
                "created_at": new_assistant.created_at.isoformat(),
            }
        }), 201 
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create assistant", "details": str(e)}), 500
    
# API to save a prompt
@app.route('/api/prompt', methods=['POST'])
def save_prompt():
    data = request.get_json()
    user_message = data.get('message')
    assistant_id = data.get('assistant_id')

    if not user_message or not assistant_id:
        return jsonify({'error': 'Message and assistant_id are required'}), 400

    # Save the prompt to the database
    new_prompt = Prompt(assistant_id=assistant_id, prompt=user_message)
    db.session.add(new_prompt)
    db.session.commit()

    return jsonify({'message': 'Prompt saved successfully'}), 201

# API for chatbot conversation
@app.route("/api/chat", methods=["POST"])
def chatbot_conversation():
    try:
        # Get the user message from the request
        data = request.json
        user_message = data.get("message")
        assistant_id = data.get("assistant_id", "default")  # Default sender if none is provided

        # Validate the message input
        if not user_message:
            return jsonify({"error": "User message is required"}), 400

        # Send the user message to the Rasa server
        response = requests.post(
            RASA_SERVER_URL,
            json={"sender": assistant_id, "message": user_message},
        )

        # Handle response from Rasa server
        if response.status_code == 200:
            rasa_responses = response.json()
            bot_response = rasa_responses[0].get("text", "") if rasa_responses else "No response"

            # Save the conversation to the database
            session_id = str(uuid.uuid4())
            new_conversion = ChatbotConversion(
                session_id=session_id,
                user_message=user_message,
                bot_response=bot_response,
            )
            db.session.add(new_conversion)
            db.session.commit()

            # Return the bot's response
            return jsonify({
                "session_id": session_id,
                "bot_message": bot_response
            })

        else:
            return jsonify({"error": "Failed to communicate with Rasa server"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
 