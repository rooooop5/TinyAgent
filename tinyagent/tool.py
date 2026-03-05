class Tool:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

    def __repr__(self):
        return f'Tool(callable={self.name})'
