from tinyagent.schema import Prompt
from typing import List

class Memory:
    def __init__(self):
        self.memory: List[dict]=[]

    def update_memory(self,prompt:Prompt):
        self.memory.append(prompt.model_dump())



