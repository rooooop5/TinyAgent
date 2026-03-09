import sqlite3


class DatabaseMemoryMangager:
    def __init__(self, agent_name: str):
        self.table_name = agent_name
        self.connection_obj = sqlite3.connect('agents_memory.db')
        self.connection_obj.row_factory = sqlite3.Row
        self._create_memory()

    def _create_memory(self):
        cursor = self.connection_obj.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS "{self.table_name}" (id INTEGER PRIMARY KEY,role TEXT,content TEXT) """
        )
        self.connection_obj.commit()

    def _append_memory(self, prompt: dict):
        cursor = self.connection_obj.cursor()
        cursor.execute(
            f"""INSERT INTO "{self.table_name}" (role,content) VALUES (?,?)""",
            (str(prompt['role']), str(prompt['content'])),
        )
        self.connection_obj.commit()

    def _load_from_memory(self):
        cursor = self.connection_obj.cursor()
        rows = cursor.execute(f"""SELECT role,content FROM "{self.table_name}" """)
        return [dict(row) for row in rows]

    def _clear_memory(self):
        cursor = self.connection_obj.cursor()
        cursor.execute(f"""DELETE FROM "{self.table_name}" """)
        self.connection_obj.commit()


class Memory:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self._database_memory_manager = DatabaseMemoryMangager(self.agent_name)
        self._messages: list[dict] = self._database_memory_manager._load_from_memory()

    @property
    def messages(self) -> list[dict]:
        return self._messages

    @messages.setter
    def messages(self, messages: list[dict]):
        self._messages = messages

    def save(self, prompt_list: list[dict]):
        for prompt in prompt_list:
            self._messages.append(prompt)

    def save_to_database(self, prompt_list: list[dict]):
        for prompt in prompt_list:
            self._database_memory_manager._append_memory(prompt)
