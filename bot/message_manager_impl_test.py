import unittest
from . import message
from .message_manager_impl import MessageManagerImpl


class TestMessageManagerImpl(unittest.TestCase):
    def generate_message(self):
        return message.Message(
            type=message.Type.TEXT,
            role=message.Role.USER,
            content=f"msg",
        )

    def test_clear(self):
        manager = MessageManagerImpl(max_size=5)
        manager.put(self.generate_message())
        manager.put(self.generate_message())
        self.assertTrue(len(manager.list()) == 2)

        manager.clear()
        self.assertTrue(len(manager.list()) == 0)

    def test_list(self):
        msgs = [self.generate_message(), self.generate_message()]

        manager = MessageManagerImpl(max_size=5)
        manager.put(msgs[0])
        manager.put(msgs[1])

        messages = manager.list()
        self.assertEqual(messages, msgs)

    def test_set_max_size(self):
        messags = [
            self.generate_message(),
            self.generate_message(),
            self.generate_message(),
        ]
        manager = MessageManagerImpl(max_size=2)
        manager.put(messags[0])
        manager.put(messags[1])
        manager.put(messags[2])
        self.assertEqual(manager.list(), messags[1:])

        manager.set_max_size(max_size=3)
        manager.put(messags[0])
        self.assertEqual(manager.list(), messags[1:] + [messags[0]])


if __name__ == "__main__":
    unittest.main()
