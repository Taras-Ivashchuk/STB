from typing import Any

from pydantic_ai import Agent, ModelMessage, ModelMessagesTypeAdapter

from models.agent import AgentResponse


class PydanticAgent:

    def __init__(
        self,
        llm_model: Any,
        output_type: Any | None = None,
    ) -> None:
        self._model = llm_model
        self._output_type = output_type
        self._agent = Agent(
            model=self._model,
            output_type=self._output_type if self._output_type is not None else str,
        )

    async def ask(self, question: str, *args, **kwargs) -> AgentResponse:
        history_as_json = kwargs.get("history")
        history = self._deserialize(history_as_json)

        result = await self._agent.run(question, message_history=history)

        return AgentResponse(
            response=result.output, history=self._serialize(result.all_messages())
        )

    @staticmethod
    def _serialize(history_as_models: list[ModelMessage]) -> bytes:
        return ModelMessagesTypeAdapter.dump_json(history_as_models)

    @staticmethod
    def _deserialize(history_as_json: str | None) -> list[ModelMessage] | None:
        if history_as_json is None:
            return None
        return ModelMessagesTypeAdapter.validate_json(history_as_json)
