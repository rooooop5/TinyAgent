from typing import Any

from pydantic import UUID4, BaseModel, Field, Json


class ToolCall(BaseModel):
    tool_name: str = Field(description='Name of the tool')
    tool_args: dict = Field(description='Mapping of tool arg name and tool arg value')


class SubAgentCall(BaseModel):
    agent_name: UUID4 = Field(description='agent_name')
    prompt: str = Field(description='Prompt for the sub agent')


class Content(BaseModel):
    response: Any | None = None
    tool_calls: list[ToolCall] = []
    sub_agent_calls: list[SubAgentCall] = []


class ModelResponse(BaseModel):
    role: str
    content: Json[Content]
    thinking: str | None = None


class Prompt(BaseModel):
    role: str
    content: Any
