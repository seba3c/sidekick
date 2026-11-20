from langchain.agents.middleware import (
    AgentMiddleware,
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    PIIMiddleware,
    TodoListMiddleware,
)
from langchain_core.messages import ToolMessage


class TolerateToolErrors(AgentMiddleware):
    """Hand tool failures back to the model as a message so it can recover, rather than
    crashing the run. Tools that touch the outside world, like a browser, fail now and then."""

    async def awrap_tool_call(self, request, handler):
        try:
            return await handler(request)
        except Exception as error:  # noqa: BLE001
            return ToolMessage(
                content=f"That tool call failed: {error}. Try another approach.",
                tool_call_id=request.tool_call["id"],
            )


def get_all_middlewares():
    return [
        TolerateToolErrors(),
        TodoListMiddleware(),
        PIIMiddleware("email"),
        PIIMiddleware("credit_card", apply_to_tool_results=True),
        ModelCallLimitMiddleware(run_limit=30),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_push_notification": True,
                "request_human_help": True,
            }
        ),
    ]
