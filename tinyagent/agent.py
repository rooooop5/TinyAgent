import uuid
from typing import Callable, Mapping, Self

from pydantic import BaseModel

from tinyagent.model import Model
from tinyagent.schema import ModelResponse,Prompt
from tinyagent.system_prompt import SystemPrompt
from tinyagent.tool import Tool
from tinyagent.memory import Memory


class Agent:
    def __init__(self, model: Model, description: str | None = None, response_type: BaseModel | None = None):
        self.model = model
        self.description = description
        self.tools: Mapping[str, Tool] = {}
        self.sub_agents: Mapping[str, Self] = {}
        self.memory=Memory()
        self.response_type = response_type
        self.system_prompt = SystemPrompt()

    def run(self, query: str):
        self.system_prompt.update_prompt(response_type=self.response_type, tools=self.tools, sub_agents=self.sub_agents)
        # if self.tools:
        #     return self._prompt_with_tool(query)
        # if self.sub_agents:
        #     return self._prompt_with_sub_agents(query)
        # if self.memory_enabled:
        return self._prompt_with_memory(query)
        #return self.model.prompt(query)
    
    # def add_system_prompt(self,query):
    #     if self.system_prompt.prompt:
    #         query=self.system_prompt.prompt+query
    #     return query



    def _prompt_with_tool(self, query: str):
        response = self.model.prompt(query)
        return self._run_tool(response)

    def _run_tool(self, tool_details: ModelResponse):
        tool_details = tool_details.message.content
        name = tool_details['tool_name']
        tool_args = tool_details['tool_args']
        tool_result = self.tools[name].func(**tool_args)
        return tool_result

    def _prompt_with_sub_agents(self, query: str):
        response = self.model.prompt(query)
        sub_agent_details = response.message.content
        sub_agent_name = sub_agent_details['agent_name']
        prompt = sub_agent_details['prompt']
        sub_agent = self.sub_agents[sub_agent_name]
        return sub_agent.run(prompt)

    def _prompt_with_memory(self, query: str):
        messages=[]
        messages.append(self.memory.memory)
        response=self.model.prompt(messages=messages.append({"role":"user","content":query}))
        self.memory.update_memory(Prompt(role="user",content=query))
        self.memory.update_memory(Prompt(role="assistant",content=response) )
        return response
        

    def add_tool(self, func: Callable) -> None:
        self.tools[func.__name__] = Tool(func.__name__, func.__doc__, func)

    def tool(self, func: Callable) -> Callable:
        self.add_tool(func)
        return func

    def add_sub_agent(self, agent: Self) -> None:
        self.sub_agents[str(uuid.uuid4())] = agent

    def __repr__(self) -> str:
        return f'Agent(model={self.model.name} tools={[tool for tool in self.tools.values()]})'
