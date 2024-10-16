from enum import Enum
from dataclasses import dataclass


class Type(Enum):
    TEXT = "Text"
    IMAGE = "Image"


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    role: Role
    type: Type
    # 当 type 为 TEXT 时，content 为文本内容
    # 当 type 为 IMAGE 时，content 为图片的 base64
    content: str
