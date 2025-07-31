from app.tool import BaseTool
import asyncio
import time
import uuid


class AskHumanWeb(BaseTool):
    """Add a tool to ask human for help via web interface."""

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

    def __init__(self):
        super().__init__()
        
    async def execute(self, inquire: str) -> str:
        try:
            # Import here to avoid circular imports
            from app.logger import logger
            from app.state import get_human_response, store_human_question
            
            # Generate unique question ID
            question_id = str(uuid.uuid4())
            
            # Store the question and wait for response
            store_human_question(question_id, inquire)
            logger.info(f"🔧 Tool 'ask_human' waiting for human response to: {inquire}")
            
            # Wait for human response with timeout
            max_wait_time = 300  # 5 minutes timeout
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                response = get_human_response(question_id)
                if response:
                    logger.info(f"✅ Received human response: {response}")
                    return response
                    
                await asyncio.sleep(1)  # Check every second
            
            # Timeout
            logger.warning(f"⏰ Human response timeout for question: {inquire}")
            return "No response received within 5 minutes. Please try again or rephrase your request."
            
        except Exception as e:
            # Fallback to original behavior for CLI environments
            from app.logger import logger
            logger.warning(f"ask_human tool error: {e}, falling back to input()")
            try:
                return input(f"""Bot: {inquire}\n\nYou: """).strip()
            except:
                return f"Unable to get human input for question: {inquire}"