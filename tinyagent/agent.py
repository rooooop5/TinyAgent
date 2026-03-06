import json
import uuid
from typing import Callable, Mapping, Self

import jinja2

from tinyagent.model import Model
from tinyagent.tool import Tool
from tinyagent.chat_history import ChatHistory

SYSTEM_PROMPT_WITH_TOOLS = """You have these tools at your disposal
---------------TOOLS---------------
{% for tool_name,tool_metadata in tools.items() %}
    Name: {{tool_name}}
    Desciption:
    {{tool_metadata.description}}
{% endfor %}

Choose the appropiate tool to use and return in the format of a mapping that includes tool_name
and the tool arguments in the format.Use valid json format
{
tool_name: name of the tool,
tool_args: {arg_name: arg_value}
}
"""


SYSTEM_PROMPT_WITH_SUB_AGENTS = """You have these agents at your disposal
---------------AGENTS---------------
{% for agent_name,agent in agents.items() %}
    Name: {{agent_name}}
    Desciption:
    {{agent.description}}
{% endfor %}

Choose the appropiate agent to use and return in the format of a mapping that includes agent_name and the prompt for
the sub agent in the format.use valid json format
{
agent_name: name of the agent,
prompt: prompt
}
"""


class Agent:
    def __init__(self, model: Model, description: str | None = None):
        self.model = model
        self.description = description
        self.tools: Mapping[str, Tool] = {}
        self.sub_agents: Mapping[str, Self] = {}
        self.context = False
        self.context = ChatHistory()

    def run(self, query: str):
        if self.tools:
            return self._prompt_with_tool(query)
        if self.sub_agents:
            return self._prompt_with_sub_agents(query)
        if self.context:
            return self._prompt_with_context(query)
        return self.model.prompt(query)

    def _prompt_with_tool(self, query: str):
        self.model.system_prompt = jinja2.Template(SYSTEM_PROMPT_WITH_TOOLS).render(tools=self.tools)
        tool_details = self.model.prompt(query)
        return self._run_tool(tool_details)

    def _run_tool(self, tool_details: dict):
        tool_details = json.loads(tool_details)
        name = tool_details['tool_name']
        tool_args = tool_details['tool_args']
        tool_result = self.tools[name].func(**tool_args)
        return tool_result

    def _prompt_with_sub_agents(self, query: str):
        self.model.system_prompt = jinja2.Template(SYSTEM_PROMPT_WITH_SUB_AGENTS).render(agents=self.sub_agents)
        sub_agent_details = self.model.prompt(query)
        sub_agent_details = json.loads(sub_agent_details)
        sub_agent_name = sub_agent_details['agent_name']
        prompt = sub_agent_details['prompt']
        sub_agent = self.sub_agents[sub_agent_name]
        return sub_agent.run(prompt)

    def _prompt_with_context(self, query: str):
        pass

    def add_tool(self, func: Callable) -> None:
        self.tools[func.__name__] = Tool(func.__name__, func.__doc__, func)

    def tool(self, func: Callable) -> Callable:
        self.add_tool(func)
        return func

    def add_sub_agent(self, agent: Self):
        self.sub_agents[str(uuid.uuid4())] = agent

    def __repr__(self):
        return f'Agent(model={self.model.name} tools={[tool for tool in self.tools.values()]})'
