"""Orchestrate worker attempts, evaluator feedback, and user approvals."""

import uuid

from evaluator import Evaluator
from langgraph.types import Command
from worker import Worker

MAX_ATTEMPTS = 3


class Sidekick:
    def __init__(self):
        self.sidekick_id = str(uuid.uuid4())
        self.worker = Worker()
        self.evaluator = Evaluator()
        self.task = ""
        self.success_criteria = ""
        self.attempts = 0
        self.paused = False
        self.pending_actions = 0
        self.todos = []

    async def setup(self):
        await self.worker.setup()
        self.evaluator.setup()

    async def run_turn(
        self, message: str, success_criteria: str, history: list
    ) -> list:
        """One turn of conversation: the worker attempts the task and the evaluator checks it,
        retrying with feedback up to MAX_ATTEMPTS. If the worker pauses for approval, this
        returns straight away with paused set, and resume() continues the same turn."""
        self.task = message
        self.success_criteria = (
            success_criteria or "The answer should be clear, correct and complete"
        )
        self.attempts = 0
        self.todos = []
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"{message}\n\nThe success criteria for this task are: {self.success_criteria}",
                }
            ]
        }
        return await self._advance(
            payload, history + [{"role": "user", "content": message}]
        )

    async def resume(self, history: list) -> list:
        """Approve the actions the worker paused on, and continue the turn."""
        payload = Command(
            resume={"decisions": [{"type": "approve"}] * self.pending_actions}
        )
        return await self._advance(payload, history)

    async def _advance(self, payload, history: list) -> list:
        config = {"configurable": {"thread_id": self.sidekick_id}}
        while True:
            result = None
            async for result in self.worker.astream(
                payload, config=config, stream_mode="values"
            ):
                self.todos = result.get("todos", self.todos)

            if "__interrupt__" in result:
                actions = result["__interrupt__"][0].value["action_requests"]
                self.paused = True
                self.pending_actions = len(actions)
                described = "\n".join(action["description"] for action in actions)
                return history + [
                    {
                        "role": "assistant",
                        "content": f"Waiting for your approval:\n{described}",
                    }
                ]

            self.paused = False
            reply = result["messages"][-1].content
            tools_used = [
                call["name"]
                for m in result["messages"]
                for call in (getattr(m, "tool_calls", None) or [])
            ]
            self.attempts += 1
            verdict = await self.evaluator.evaluate(
                self.task, self.success_criteria, reply, tools_used
            )
            if (
                verdict.success_criteria_met
                or verdict.user_input_needed
                or self.attempts >= MAX_ATTEMPTS
            ):
                return history + [
                    {"role": "assistant", "content": reply},
                    {"role": "assistant", "content": f"Evaluator: {verdict.feedback}"},
                ]
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Your last response did not meet the success criteria. "
                        f"Here is the feedback: {verdict.feedback}. Please keep working and address it.",
                    }
                ]
            }

    def cleanup(self):
        """Shut down the MCP servers; the browser window closes."""
        self.worker.cleanup()
