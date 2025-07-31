# app/state.py
"""Shared application state management"""

from typing import Dict, Any
from threading import Lock
import time

# Global state for running tasks
running_tasks: Dict[str, Dict[str, Any]] = {}
_tasks_lock = Lock()

def create_task(task_id: str) -> None:
    """Create a new task entry"""
    with _tasks_lock:
        running_tasks[task_id] = {
            'stop_flag': False,
            'start_time': time.time()
        }

def stop_task(task_id: str) -> bool:
    """Set stop flag for a task"""
    with _tasks_lock:
        if task_id in running_tasks:
            running_tasks[task_id]['stop_flag'] = True
            return True
        return False

def is_task_stopped(task_id: str) -> bool:
    """Check if a task has been stopped"""
    with _tasks_lock:
        return running_tasks.get(task_id, {}).get('stop_flag', False)

def cleanup_task(task_id: str) -> None:
    """Remove a task from tracking"""
    with _tasks_lock:
        running_tasks.pop(task_id, None)

def get_task_info(task_id: str) -> Dict[str, Any]:
    """Get task information"""
    with _tasks_lock:
        return running_tasks.get(task_id, {}).copy()
# Global state for human questions/responses
human_questions: Dict[str, str] = {}  # question_id -> question
human_responses: Dict[str, str] = {}  # question_id -> response
_human_lock = Lock()

# Human question/response functions
def store_human_question(question_id: str, question: str) -> None:
    """Store a question waiting for human response"""
    with _human_lock:
        human_questions[question_id] = question

def get_human_response(question_id: str) -> Optional[str]:
    """Get human response for a question"""
    with _human_lock:
        return human_responses.get(question_id)

def submit_human_response(question_id: str, response: str) -> bool:
    """Submit a human response to a question"""
    with _human_lock:
        if question_id in human_questions:
            human_responses[question_id] = response
            return True
        return False

def get_pending_questions() -> Dict[str, str]:
    """Get all pending questions"""
    with _human_lock:
        return human_questions.copy()

def cleanup_human_interaction(question_id: str) -> None:
    """Clean up human question/response"""
    with _human_lock:
        human_questions.pop(question_id, None)
        human_responses.pop(question_id, None)

# Global state for human questions/responses
human_questions: Dict[str, str] = {}  # question_id -> question
human_responses: Dict[str, str] = {}  # question_id -> response
_human_lock = Lock()

# Human question/response functions
def store_human_question(question_id: str, question: str) -> None:
    """Store a question waiting for human response"""
    with _human_lock:
        human_questions[question_id] = question

def get_human_response(question_id: str) -> Optional[str]:
    """Get human response for a question"""
    with _human_lock:
        return human_responses.get(question_id)

def submit_human_response(question_id: str, response: str) -> bool:
    """Submit a human response to a question"""
    with _human_lock:
        if question_id in human_questions:
            human_responses[question_id] = response
            return True
        return False

def get_pending_questions() -> Dict[str, str]:
    """Get all pending questions"""
    with _human_lock:
        return human_questions.copy()

def cleanup_human_interaction(question_id: str) -> None:
    """Clean up human question/response"""
    with _human_lock:
        human_questions.pop(question_id, None)
        human_responses.pop(question_id, None)
