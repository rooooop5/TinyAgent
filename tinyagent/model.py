import os
import requests

from tinyagent.response import ModelResponse


class Model:
    def __init__(self, name: str, system_prompt: str | None = None):
        self.name = name

    def prompt(self, query: str):
        messages = [{'role': 'user', 'content': query}]
        data = {
            'model': self.name,
            'messages': messages,
            'stream': False,
            'format': 'json',
            'options': {'temperature': 0},
        }
        with requests.post(
            'https://ollama.com/api/chat', json=data, headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
        ) as response:
            model_response = ModelResponse(**response.json())
            return model_response
