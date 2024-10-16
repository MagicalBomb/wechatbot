from typing import List
from openai import OpenAI

from bot.message import Message
from bot.message import Type as MessageType
from bot.message import Role as MessageRole


class OpenAIChatter:
    def __init__(self, api_key: str):
        self._client = OpenAI(api_key=api_key)

        self._model = "gpt-4o-mini"
        self._system_prompt = "你是一个群聊助手，你的任务是帮助用户回答问题。"

    def set_model(self, model: str):
        self._model = model

    def get_model(self) -> str:
        return self._model

    def set_prompt(self, prompt: str):
        self._system_prompt = prompt

    def get_prompt(self) -> str:
        return self._system_prompt

    def models(self) -> List[str]:
        return ["gpt-4o-mini", "gpt-3.5-turbo"]

    def chat(self, context: List[Message]) -> Message:
        messages = self._build_messages(context)

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            n=1,
            temperature=0.3,
            top_p=1,
        )
        return Message(
            role=MessageRole.ASSISTANT,
            type=MessageType.TEXT,
            content=response.choices[0].message.content,
        )

    def _build_messages(self, context: List[Message]) -> List[dict]:
        messages = [{"role": "system", "content": self._system_prompt}]
        for m in context:
            role = {
                MessageRole.USER: "user",
                MessageRole.ASSISTANT: "assistant",
                MessageRole.SYSTEM: "system",
            }[m.role]

            if m.type == MessageType.TEXT:
                messages.append(
                    {
                        "role": role,
                        "content": [
                            {
                                "type": "text",
                                "text": m.content,
                            }
                        ],
                    }
                )
            elif m.type == MessageType.IMAGE:
                messages.append(
                    {
                        "role": role,
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": m.content,
                                },
                            }
                        ],
                    }
                )
            else:
                raise ValueError(f"Unsupported message type: {m.type}")
        return messages
