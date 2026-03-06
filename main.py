from tinyagent import Agent, Model
from tinyagent.chat_history import ChatHistory
import os
if __name__ == '__main__':
    # model = Model('gpt-oss:120b')
    # model = Model('gemini-3-flash-preview:latest')
    # agent = Agent(model)
    # sub_agent = Agent(model, description='This agent is able to do maths')

    # @sub_agent.tool
    # def add_numbers(a: int, b: int) -> int:
    #     """This tool given two numbers returns the sum of the numbers

    #     Args:
    #         a (int): number
    #         b (int): number

    #     Returns:
    #         int: sum of a and b
    #     """
    #     return a + b

    # @agent.tool
    # def get_current_time() -> str:
    #     """Return the current server time."""
    #     return str(datetime.now())

    # @agent.tool
    # def max_number(numbers: list[int]) -> int:
    #     """Return largest number from a list."""
    #     return max(numbers)

    # agent.add_sub_agent(sub_agent)

    # print(agent.run('Add 2 and 6'))
    print(os.getenv("OLLAMA_API_KEY"))
    my_model=Model('gemini-3-flash-preview:latest')
    chat_history=ChatHistory()
    print(my_model.prompt("What is your name?",chat_history=chat_history))
    print(chat_history.history)
    