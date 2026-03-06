from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str

    def message_dump(self):
        return {'role': self.role, 'content': self.content}
