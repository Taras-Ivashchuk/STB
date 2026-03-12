from typing import Protocol

from models.agent import AgentResponse


class AgentInterface(Protocol):
    async def ask(self, question: str, *args, **kwargs) -> AgentResponse:
        """Send the question and return the agent's answer."""
        ...
