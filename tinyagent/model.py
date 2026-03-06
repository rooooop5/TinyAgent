import os
from pprint import pprint
from tinyagent.chat_history import ChatHistory
from tinyagent.message import Message
import requests


class Model:
    def __init__(self, name: str, system_prompt: str | None = None):
        self.name = name
        self.system_prompt = system_prompt

    def prompt(self, query: str, chat_history: ChatHistory | None):
        user_message = Message(role='user', content=query)
        chat_history.update_history(user_message)
        if self.system_prompt and not chat_history.is_sysytem_prompt_present():
            chat_history.update_history(Message(role='system', content=self.system_prompt))
        data = {'model': self.name, 'messages': chat_history.history, 'stream': False}
        with requests.post(
            'https://ollama.com/api/chat', json=data, headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
        ) as response:
            r = response.json()
            pprint(r, indent=2)
            content = r['message']['content']
            chat_history.update_history(Message(role='assistant', content=content))
            return content
