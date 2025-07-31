from app.tool import BaseTool
from app.logger import logger
import os
import json

class AskHuman(BaseTool):
    """Add a tool to ask human for help (web-compatible)."""

    name: str = "ask_human"
    description: str = "Use this tool to ask human for help."
    parameters: str = {
        "type": "object",
        "properties": {
            "inquire": {
                "type": "string",
                "description": "The question you want to ask human.",
            }
        },
        "required": ["inquire"],
    }

    async def execute(self, inquire: str, chat_id: str = None) -> str:
        # For web: store the pending question in the chat session and return a special marker
        if not chat_id:
            logger.error("AskHuman tool called without chat_id!")
            return "[ask_human: error - no chat_id]"
        # Store pending question in chat session
        chat_sessions_file = 'chat_sessions.json'
        if os.path.exists(chat_sessions_file):
            with open(chat_sessions_file, 'r', encoding='utf-8') as f:
                sessions = json.load(f)
        else:
            sessions = {}
        if chat_id not in sessions:
            sessions[chat_id] = {
                'messages': [],
                'status': 'created',
                'created_at': '',
                'last_update': '',
                'process_status': 'waiting_human',
                'agent_type': 'manus',
                'uploaded_files': []
            }
        sessions[chat_id]['messages'].append({
            'sender': 'agent',
            'text': f"[ask_human] {inquire}",
            'files': [],
            'timestamp': ''
        })
        sessions[chat_id]['process_status'] = 'waiting_human'
        with open(chat_sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
        return f"[ask_human] {inquire}"
