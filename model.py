from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database object
db = SQLAlchemy()

# Define the Assistant Model
class Assistant(db.Model):
    __tablename__ = 'Assistants'  # Exact table name from PostgreSQL
    __table_args__ = {'schema': 'public'}  # Specify schema as public

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Assistant {self.name}>'

# Additional models can be added as needed
# Define the Prompt Model
# class Prompt(db.Model):
#     __tablename__ = 'Prompts'  
#     __table_args__ = {'schema': 'public'}  # Use the 'public' schema for PostgreSQL

#     id = db.Column(db.Integer, primary_key=True)
#     assistant_id = db.Column(db.Integer, db.ForeignKey('Assistants.id'), nullable=False)
#     prompt = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     assistant = db.relationship('Assistant', backref='prompts', lazy=True)

#     def __repr__(self):
#         return f'<Prompt {self.prompt}>'
class Prompt(db.Model):
    __tablename__ = 'Prompts'  
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    assistant_id = db.Column(db.Integer, db.ForeignKey('public.Assistants.id'), nullable=False)
    prompt = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # assistant = db.relationship('Assistant', backref='prompts')

    def __init__(self, assistant_id, prompt):
        self.assistant_id = assistant_id
        self.prompt = prompt

# Define the Chatbot Conversion Model
class ChatbotConversion(db.Model):
    __tablename__ = 'chatbot_conversions'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=False)  # UUID format
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<ChatbotConversion session_id={self.session_id}>'