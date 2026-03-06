from tinyagent.schema import Prompt
from typing import List


class Memory:
    def __init__(self):
        self.messages: list[dict] = []

    def update(self, prompt: Prompt):
        self.messages.append(prompt.model_dump())
