import ast
import re
from abc import ABC
from typing import Dict, List

class ChatResponse(ABC):
    def __init__(self, content: str, total_tokens: int) -> None:
        self.content = content
        self.total_tokens = total_tokens
    
    def __repr__(self) -> str:
        return f"ChatResponse(content={self.content}, total_tokens={self.total_tokens})"

class BaseLLM(ABC):
    def __init__(self):
        pass

    def chat(self, messages: List[Dict]) -> ChatResponse:
        pass

    @staticmethod
    def literal_eval(response_content: str):
        response_content = response_content.strip()

        # remove content between <think> and </think>, especial for DeepSeek reasoning model
        if "<think>" and "</think>" in response_content:
            end_of_think = response_content.find("</think>") + len("</think>")
            response_content = response_content[end_of_think:]

        # If it's a code block, parse its contents
        if response_content.startswith("```") and response_content.endswith("```"):
            if response_content.startswith("```python"):
                response_content = response_content[9:-3]
            elif response_content.startswith("```json"):
                response_content = response_content[7:-3]
            elif response_content.startswith("```str"):
                response_content = response_content[6:-3]
            elif response_content.startswith("```\n"):
                response_content = response_content[4:-3]
            else:
                raise ValueError("Invalid code block format")
            
            try:
                return ast.literal_eval(response_content.strip())
            except:
                pass

        # Try to find and parse JSON/List content
        matches = re.findall(r'(\[.*?\]|\{.*?\})', response_content, re.DOTALL)
        if matches:
            try:
                return ast.literal_eval(matches[0])
            except:
                pass

        # If no special format is detected, return the plain text
        return response_content.strip()
