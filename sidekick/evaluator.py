"""Evaluate the worker's answer against the user's success criteria."""

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from settings import settings


class EvaluatorOutput(BaseModel):
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field(
        description="Whether the success criteria have been met"
    )
    user_input_needed: bool = Field(
        description="True if the assistant has a question, needs clarification, or is stuck and needs the user"
    )


class Evaluator:
    def __init__(self):
        self.model = None

    def setup(self):
        self.model = init_chat_model(settings.evaluator_model).with_structured_output(
            EvaluatorOutput
        )

    async def evaluate(
        self,
        message: str,
        success_criteria: str,
        last_reply: str,
        tools_used: list[str],
    ) -> EvaluatorOutput:
        prompt = f"""You decide whether an assistant has met the success criteria for a task.

The user's request was:
{message}

The success criteria are:
{success_criteria}

The tools the assistant called while working, in order:
{", ".join(tools_used) or "none"}

The assistant's most recent reply was:
{last_reply}

Decide whether the success criteria are met, using the tool calls as evidence of what was actually done.
Also decide whether the assistant needs more input from the user, either because it asked a question,
needs clarification, or seems stuck. Give brief, concrete feedback."""
        return await self.model.ainvoke(prompt)
