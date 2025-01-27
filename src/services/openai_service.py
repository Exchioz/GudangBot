from openai import OpenAI
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://api.openai.com/v1/",
            api_key=api_key
        )
    
    def create_completion(
        self, 
        messages: List[Dict[str, str]], 
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Dict[str, str]] = None
    ) -> Any:
        try:
            params = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
            }
            if functions:
                params["functions"] = functions
            if function_call:
                params["function_call"] = function_call
                
            return self.client.chat.completions.create(**params)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise