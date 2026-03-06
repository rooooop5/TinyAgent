import jinja2
from pydantic import BaseModel

#from tinyagent.schema import SubAgentResponse, ToolResponse

SYSTEM_PROMPT = """Response schema: {{response_schema}}"""

SYSTEM_PROMPT_WITH_TOOLS = """You have these tools at your disposal
---------------TOOLS---------------
{% for tool_name,tool_metadata in tools.items() %}
    Name: {{tool_name}}
    Desciption:
    {{tool_metadata.description}}
{% endfor %}

Choose the appropiate tool to use

Response schema: {{response_schema}}
"""


SYSTEM_PROMPT_WITH_SUB_AGENTS = """You have these agents at your disposal
---------------AGENTS---------------
{% for agent_name,agent in agents.items() %}
    Name: {{agent_name}}
    Desciption:
    {{agent.description}}
{% endfor %}

Choose the appropiate agent to use

Response schema: {{response_schema}}
"""


class SystemPrompt:
    def __init__(self, prompt: str | None = None):
        self.prompt = '' if not prompt else prompt

    def update_prompt(
        self, response_type: BaseModel | None = None, tools: dict | None = None, sub_agents: dict | None = None
    ):
        if response_type:
            self.prompt += '\n' + jinja2.Template(SYSTEM_PROMPT).render(
                response_schema=response_type.model_json_schema()
            )
        if tools:
            self.prompt += '\n' + jinja2.Template(SYSTEM_PROMPT_WITH_TOOLS).render(
                tools=tools, response_schema=ToolResponse.model_json_schema()
            )
        if sub_agents:
            self.prompt += '\n' + jinja2.Template(SYSTEM_PROMPT_WITH_SUB_AGENTS).render(
                agents=sub_agents, response_schema=SubAgentResponse.model_json_schema()
            )
