"""
Database module for chat history and session management
"""
import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading

class ChatDatabase:
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """Initialize the database tables"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Chat sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    shareable_url TEXT UNIQUE
                )
            """)
            
            # Chat messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_message TEXT,
                    agent_response TEXT,
                    agent_type TEXT DEFAULT 'manus',
                    uploaded_files TEXT,
                    message_order INTEGER,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions (id)
                )
            """)
            
            conn.commit()
            conn.close()
    
    def create_session(self, title: Optional[str] = None) -> Dict[str, str]:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        shareable_url = f"/chat/{session_id}"
        
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO chat_sessions (id, title, shareable_url) VALUES (?, ?, ?)",
                (session_id, title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}", shareable_url)
            )
            
            conn.commit()
            conn.close()
        
        return {'session_id': session_id, 'shareable_url': shareable_url}
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT 1 FROM chat_sessions WHERE id = ?", (session_id,))
            exists = cursor.fetchone() is not None
            
            conn.close()
            return exists

# Global database instance
db = ChatDatabase()

# Helper functions for backward compatibility
def load_chat_history():
    return []

def save_chat_history(chat_data):
    pass
