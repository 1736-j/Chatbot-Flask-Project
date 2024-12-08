import os

class Config:
    # PostgreSQL Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass#123@localhost:5432/sensiaproject'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy's event system
    
    # OpenAI API Key
    OPENAI_API_KEY = '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'

    # Secret Key for session management
    SECRET_KEY = 'your-secret-key'

    # CORS settings
    CORS_ALLOWED_ORIGINS = ['http://localhost:3000']  # Adjust as needed
