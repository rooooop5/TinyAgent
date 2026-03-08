from tinyagent.schema import Prompt
from typing import List
import sqlite3


class DatabaseMemoryMangager:
    def __init__(self, agent_name: str):
        self.table_name = agent_name
        self.connection_obj = sqlite3.connect('agents_memory.db')
        self.connection_obj.row_factory = sqlite3.Row

    def _create_memory(self):
        cursor = self.connection_obj.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name}(id INTEGER PRIMARY KEY,role TEXT,content TEXT) """
        )
        self.connection_obj.commit()

    def _append_memory(self, prompt: dict):
        cursor = self.connection_obj.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table_name} (role,content) VALUES (?,?)""",
            (str(prompt['role']), str(prompt['content'])),
        )
        self.connection_obj.commit()

    def _load_from_memory(self):
        cursor = self.connection_obj.cursor()
        cursor.execute(f"""SELECT * FROM {self.table_name}""")
        return [dict(row) for row in cursor.fetchall()]


class Memory:
    def __init__(self, agent_name):
        self.database_memory_manager = DatabaseMemoryMangager(agent_name)   
        self.database_memory_manager._create_memory() 
        self.messages: list[dict] = self.database_memory_manager._load_from_memory()
        

    def update(self, prompt: Prompt):
        self.messages.append(prompt.model_dump())
        self.database_memory_manager._append_memory(prompt.model_dump())
