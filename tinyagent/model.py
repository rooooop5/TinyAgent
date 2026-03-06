import os
import requests

from tinyagent.schema import ModelResponse


class Model:
    def __init__(self, name: str, system_prompt: str | None = None):
        self.name = name

    def prompt(self, messages: list):
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
