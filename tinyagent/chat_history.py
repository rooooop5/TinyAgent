from tinyagent.message import Message


class ChatHistory:
    def __init__(self):
        self.history: list[dict] = []

    def update_history(self, message: Message):
        self.history.append(message.message_dump())

    def is_sysytem_prompt_present(self):
        for message in self.history:
            if message['role'] == 'system':
                return True
        return False


