import os
from .message import Message
from .bot import Bot
from .chattter.openai import OpenAIChatter
from .message_manager_impl import MessageManagerImpl

api_key = os.getenv("OPENAI_API_KEY")

_message_manager_impl = MessageManagerImpl(max_size=20)
_chatter_impl = OpenAIChatter(
    api_key=api_key,
)
bot = Bot(chatter=_chatter_impl, message_manager=_message_manager_impl)
