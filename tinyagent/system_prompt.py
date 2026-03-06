import jinja2
from pydantic import BaseModel

from tinyagent.schema import Prompt,Content
SYSTEM_PROMPT_WITHOUT_RESPONSE_FORMAT = """ Follow this schema for generating responses
Response schema: {{response_schema}}

Populate the response field to give simple response or when you have the final response
Populate the tool_calls field if you need to call any tools
Populate the sub_agent_calls field if you to call any sub agents
Use the exit field when you think you have gathered the information and is ready to respond.
"""

SYSTEM_PROMPT_WITH_RESPONSE_FORMAT=""" Follow this schema for generating responses
Response schema: {{response_schema}}

Populate the response field to give simple response or when you have the final response
When populating the "response" field, the value MUST strictly follow this schema:

{{response_format}}

Rules:
- The response must be valid JSON.
- Do not include any explanations or text outside the JSON.
- All fields defined in the schema must follow their specified types.
- Do not add extra fields.

Populate the tool_calls field if you need to call any tools
Populate the sub_agent_calls field if you to call any sub agents
Use the exit field when you think you have gathered the information and is ready to respond.
"""

TOOL_DEFINATIONS = """You have these tools at your disposal
---------------TOOLS---------------
{% for tool_name,tool_metadata in tools.items() %}
    Name: {{tool_name}}
    Desciption:
    {{tool_metadata.description}}
{% endfor %}

Choose the appropiate tool to use


"""


SUB_AGENTS_DEFINATIONS = """You have these agents at your disposal
---------------AGENTS---------------
{% for agent_name,agent in agents.items() %}
    Name: {{agent_name}}
    Desciption:
    {{agent.description}}
{% endfor %}

Choose the appropiate agent to use
"""


def generate_system_prompt(
    system_prompt: Prompt | None = None,
    response_type: BaseModel | None = None,
    tools: dict | None = None,
    sub_agents: dict | None = None,
) -> Prompt:
    system_prompt = Prompt(role='system', content='')
    if response_type:
        system_prompt.content += '\n' + jinja2.Template(SYSTEM_PROMPT_WITH_RESPONSE_FORMAT).render(response_schema=Content.model_json_schema(),
            response_format=response_type.model_json_schema()
        )
    else:
        system_prompt.content+='\n' + jinja2.Template(SYSTEM_PROMPT_WITHOUT_RESPONSE_FORMAT).render(response_schema=Content.model_json_schema())
    if tools:
        system_prompt.content += '\n' + jinja2.Template(TOOL_DEFINATIONS).render(tools=tools)
    if sub_agents:
        system_prompt.content += '\n' + jinja2.Template(SUB_AGENTS_DEFINATIONS).render(agents=sub_agents)
    return system_prompt
