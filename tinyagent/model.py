import os
from pprint import pprint

import requests


class Model:
    def __init__(self, name: str, system_prompt: str | None = None):
        self.name = name
        self.system_prompt = system_prompt

    def prompt(self, query: str):
        messages = [{'role': 'user', 'content': query}]
        if self.system_prompt:
            messages.append({'role': 'system', 'content': self.system_prompt})
        data = {'model': self.name, 'messages': messages, 'stream': False}
        with requests.post(
            'https://ollama.com/api/chat', json=data, headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
        ) as response:
            r = response.json()
            pprint(r, indent=2)
            content = response.json()['message']['content']
            return content
