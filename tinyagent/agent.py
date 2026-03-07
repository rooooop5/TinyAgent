import uuid
from typing import Callable, Mapping, Self

from pydantic import BaseModel, ValidationError

from tinyagent.model import Model
from tinyagent.schema import ModelResponse, Prompt
from tinyagent.system_prompt import generate_system_prompt
from tinyagent.tool import Tool
from tinyagent.memory import Memory


class Agent:
    def __init__(
        self,
        model: Model,
        system_prompt: Prompt | str | None = None,
        description: str | None = None,
        response_format: BaseModel | None = None,
    ):
        self.model = model
        self.description = description
        self.tools: Mapping[str, Tool] = {}
        self.sub_agents: Mapping[str, Self] = {}
        self.memory = Memory()
        self.response_format = response_format

        if system_prompt and isinstance(system_prompt, str):
            system_prompt = Prompt(role='system', content=system_prompt)
        else:
            system_prompt = Prompt(role='system', content='')

        self.system_prompt = system_prompt

    def run(self, prompt: str):
        if self.response_format:
            self.system_prompt + (
                generate_system_prompt(
                    system_prompt=self.system_prompt,
                    response_type=self.response_format,
                    tools=self.tools,
                    sub_agents=self.sub_agents,
                )
            )
        else:
            self.system_prompt + (
                generate_system_prompt(system_prompt=self.system_prompt, tools=self.tools, sub_agents=self.sub_agents)
            )
        user_prompt = Prompt(role='user', content=prompt)
        self.memory.update(self.system_prompt)
        self.memory.update(user_prompt)

        resp = self._loop()
        return resp

    def _loop(self):
        while True:
            resp = self._get_valid_response()
            if resp.content.exit:
                return resp.content.response

            self.memory.update(Prompt(role=resp.role, content=resp.content.model_dump_json()))

            if resp.content.tool_calls:
                for tool_call in resp.content.tool_calls:
                    tool_name = tool_call.tool_name
                    tool_args = tool_call.tool_args
                    tool_result = self.tools[tool_name].func(**tool_args)
                    self.memory.update(Prompt(role='tool', content=str(tool_result)))

            if resp.content.sub_agent_calls:
                for sub_agent_call in resp.content.sub_agent_calls:
                    sub_agent_name = sub_agent_call.agent_name
                    sub_agent_prompt = sub_agent_call.prompt
                    sub_agent = self.sub_agents[sub_agent_name]
                    sub_agent_resp = sub_agent.run(sub_agent_prompt)
                    self.memory.update(Prompt(role='tool', content=sub_agent_resp))

    def _get_valid_response(self):
        for _ in range(3):
            resp: ModelResponse = self.model.prompt(self.memory.messages)
            if not self.response_format:
                return resp
            if self._validate_response_format(resp.content.response):
                return resp
        raise ValueError('Unable to provide structured output')

    def _validate_response_format(self, response):
        try:
            self.response_format.model_validate(response)
            return True
        except ValidationError:
            return False

    def add_tool(self, func: Callable) -> None:
        self.tools[str(uuid.uuid4())] = Tool(func.__name__, func.__doc__, func)

    def tool(self, func: Callable) -> Callable:
        self.add_tool(func)
        return func

    def add_sub_agent(self, agent: Self) -> None:
        self.sub_agents[str(uuid.uuid4())] = agent

    def __repr__(self) -> str:
        return f'Agent(model={self.model.name} tools={[tool for tool in self.tools.values()]})'
