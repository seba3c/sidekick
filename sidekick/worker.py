"""Worker agent and the resources it uses to complete tasks."""

import os
from datetime import datetime

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from middleware import get_all_middlewares
from settings import settings
from tools import get_all_tools

HERE = os.path.dirname(os.path.abspath(__file__))
SANDBOX = os.path.join(HERE, "sandbox")


WORKER_PROMPT = """You are Sidekick, a capable personal assistant who completes tasks for the user.
You have a real web browser, a sandbox filesystem, web search, Wikipedia, and the ability to send push notifications.
When you use the browser, navigate to a page and read it with a snapshot rather than clicking around unnecessarily.
Dismiss cookie banners and popups yourself by clicking in the browser. If you reach something only a human can do,
like logging in, a captcha, or two-factor authentication, use the request_human_help tool to tell the user exactly
what to do in your browser window, then carry on once they have done it.
For flight searches, use Google Flights in your browser: go straight to https://www.google.com/travel/flights?q=...
with a natural language query like "flights from New York to London leaving 14 July returning 21 July".
Keep working on the task until the success criteria are met, or until you genuinely need to ask the user a question.
If you have a question, ask it plainly. When you are finished, give your final answer clearly,
saying what you did, what you produced, and what you found."""


class Worker:
    def __init__(self):
        self.memory = InMemorySaver()
        self.tools = None
        self.sessions = None
        self.agent = None

    async def setup(self):
        os.makedirs(SANDBOX, exist_ok=True)
        self.tools, self.sessions = await get_all_tools(SANDBOX)
        self.agent = create_agent(
            model=settings.worker_model,
            tools=self.tools,
            system_prompt=self.get_system_prompt(),
            middleware=get_all_middlewares(),
            checkpointer=self.memory,
        )

    def get_system_prompt(self):
        return f"{WORKER_PROMPT}\nToday is {datetime.now():%A %d %B %Y}."

    def astream(self, payload, config, stream_mode="values"):
        """Stream agent state, including todos and approval interrupts."""
        return self.agent.astream(payload, config=config, stream_mode=stream_mode)

    def cleanup(self):
        """Shut down the MCP servers; the browser window closes."""
        if self.sessions:
            self.sessions.stop()
