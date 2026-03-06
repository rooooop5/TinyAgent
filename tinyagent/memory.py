from tinyagent.response import Prompt
from typing import List

class Memory:
    def __init__(self):
        self.memory: List[Prompt]

    def update_memory(self,prompt:Prompt):
        self.memory.append(prompt)



