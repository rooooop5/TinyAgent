from pydantic import BaseModel, Field, Json
from typing import Any


class ToolCall(BaseModel):
    tool_name: str = Field(description='Name of the tool')
    tool_args: dict = Field(description='Mapping of tool arg name and tool arg value')


class SubAgentCall(BaseModel):
    agent_name: str = Field(description='agent_name')
    prompt: str = Field(description='Prompt for the sub agent')


class Content(BaseModel):
    response: Any | None = Field(default=None, description='Response')
    tool_calls: list[ToolCall] = Field(default=[], description='list of tool calls')
    sub_agent_calls: list[SubAgentCall] = Field(default=[], description='list of sub agent calls')
    exit: bool = Field(default=False, description='Continue evaluation or not')


class ModelResponse(BaseModel):
    role: str
    content: Json[Content]
    thinking: str | None = None


class Prompt(BaseModel):
    role: str
    content: str
        
    def __add__(self,other:Prompt):
        self.content += self.content + '\n' + other.content
