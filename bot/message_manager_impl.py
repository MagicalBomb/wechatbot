import threading
from collections import deque
from .message import Message


class MessageManagerImpl:
    def __init__(self, max_size=10) -> None:
        self._queue = deque(maxlen=max_size)
        self._lock = threading.Lock()

    def clear(self) -> None:
        self._queue.clear()

    def list(self) -> list:
        return list(self._queue)

    def put(self, message: Message) -> None:
        self._queue.append(message)

    def set_max_size(self, max_size: int) -> None:
        self._lock.acquire()
        self._queue = deque(self._queue, maxlen=max_size)
        self._lock.release()

    def get_max_size(self) -> int:
        return self._queue.maxlen
