from abc import abstractmethod, ABC
from typing import List

from .message import Message


class Chatter(ABC):
    def models(self) -> List[str]: ...

    @abstractmethod
    def set_model(self, model: str): ...

    @abstractmethod
    def get_model(self) -> str: ...

    @abstractmethod
    def set_prompt(self, prompt: str): ...

    @abstractmethod
    def get_prompt(self) -> str: ...

    @abstractmethod
    def chat(self, context: List[Message]) -> Message: ...


class MessageManager(ABC):
    @abstractmethod
    def put(self, message: Message): ...

    @abstractmethod
    def clear(self): ...

    @abstractmethod
    def list(self) -> List[Message]: ...

    @abstractmethod
    def set_max_size(self, rotation: int): ...

    @abstractmethod
    def get_max_size(self) -> int: ...


class Bot:
    def __init__(self, chatter: Chatter, message_manager: MessageManager):
        self._message_manager = message_manager
        self._chatter = chatter

    def input(self, message: Message):
        self._message_manager.put(message)

    def output(self) -> Message:
        m = self._chatter.chat(context=self._message_manager.list())
        self._message_manager.put(m)
        return m

    def clear_message_history(self):
        self._message_manager.clear()

    def models(self) -> List[str]:
        return self._chatter.models()

    def messages(self) -> List[Message]:
        return self._message_manager.list()

    # 设置可以记录的最大消息数量
    def set_memory_size(self, size: int):
        self._message_manager.set_max_size(size)

    def get_memory_size(self) -> int:
        return self._message_manager.get_max_size()

    def get_ai_model(self) -> str:
        return self._chatter.get_model()

    def get_ai_prompt(self) -> str:
        return self._chatter.get_prompt()

    def set_ai_model(self, model: str):
        self._chatter.set_model(model)

    def set_ai_prompt(self, prompt: str):
        self._chatter.set_prompt(prompt)
