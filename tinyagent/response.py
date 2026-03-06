from datetime import datetime
from typing import Any

from pydantic import UUID4, BaseModel, Field, Json


class Message(BaseModel):
    role: str
    content: Json[Any]
    thinking: str | None = None


class ModelResponse(BaseModel):
    message: Message
    model: str
    prompt_eval_count: int
    total_duration: int
    done_reason: str
    done: bool
    eval_count: int
    created_at: datetime


class ToolResponse(BaseModel):
    tool_name: str = Field(description='Name of the tool')
    tool_args: dict = Field(description='Mapping of tool arg name and tool arg value')


class SubAgentResponse(BaseModel):
    agent_name: UUID4 = Field(description='agent_name')
    prompt: str = Field(description='Prompt for the sub agent')
