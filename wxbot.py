import base64
import datetime
import os
import platform
from typing import List
from lib import itchat
from lib.itchat.content import TEXT, PICTURE, RECORDING
from bot import bot
from bot import message


# 可用的二维码生成接口
# https://api.qrserver.com/v1/create-qr-code/?size=400×400&data=https://www.abc.com
# https://api.isoyu.com/qr/?m=1&e=L&p=20&url=https://www.abc.com
def qrCallback(uuid, status, qrcode):
    # logger.debug("qrCallback: {} {}".format(uuid,status))
    if status == "0":

        import qrcode

        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = (
            "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(
                url
            )
        )
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(
            url
        )
        print("You can also scan QRCode in any website below:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)


class WechatBot:
    def __init__(self):
        self._chat_bot = bot
        self._run_at = datetime.datetime.now()

        itchat.msg_register([TEXT, PICTURE], isGroupChat=True)(
            self._on_message_received
        )

    def run(self):
        itchat.auto_login(
            enableCmdQR=2,
            hotReload=True,
            statusStorageDir="itchat.pkl",
            qrCallback=qrCallback,
        )

        self._run_at = datetime.datetime.now()
        # start a thread to run following function
        # itchat.start_receiving()
        itchat.run(True)

    # 运行时间
    def run_time_str(self) -> str:
        diff = datetime.datetime.now() - self._run_at
        s = ""
        if diff.days > 0:
            s += f"{diff.days} 天 "
        if diff.seconds // 3600 > 0:
            s += f"{diff.seconds // 3600} 小时 "
        s += f"{diff.seconds % 3600} 秒"
        return s

    def on_receive_user_text(self, msg):
        user_text = msg.text
        self_nick_name = msg.user.self.nickName

        if msg.IsAt:
            user_text = user_text.replace(f"@{self_nick_name}", "").strip()

        print("Receive User Text: ", user_text)

        if user_text.strip() != "":
            self._chat_bot.input(
                message.Message(
                    type=message.Type.TEXT, role=message.Role.USER, content=msg.text
                )
            )

        if msg.IsAt:
            m = self._chat_bot.output()
            msg.user.send(m.content)

    def on_receive_user_image(self, msg):
        img_bytes = msg.text()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        img_suffix = msg.fileName.split(".")[-1]

        print("Receive User Image: ", msg.fileName, img_suffix)

        self._chat_bot.input(
            message.Message(
                type=message.Type.IMAGE,
                role=message.Role.USER,
                content=f"data:image/{img_suffix};base64,{img_base64}",
            )
        )

    def on_receive_command(self, msg, cmd: str, args: List[str]):
        if cmd == "help":
            # 运行时间: 1 天 24 小时 36 秒
            msg.user.send(
                f"""
你好，我是 chatgpt 聊天机器人
我会做多保持 {self._chat_bot.get_memory_size()} 条聊天上下文, @ 我可以回答任何问题

AI服务:  OpenAI 
模型:    {self._chat_bot.get_ai_model()}
系统预设: {self._chat_bot.get_ai_prompt()}

启动时间: {self._run_at.strftime("%Y-%m-%d %H:%M:%S")} 
运行时间: {self.run_time_str()} 
=======
/clear                      
清空上下文

/set-model {{model}}        
设置聊天模型

/set-x {{context-length}}   
设置聊天上下文的保持长度

/debug
打印调试信息
"""
            )
            return

        if cmd == "clear":
            self._chat_bot.clear_message_history()
            msg.user.send("已清空聊天上下文")
            return

        if cmd == "set-model":
            if len(args) == 0:
                msg.user.send("请输入模型名称. 例如: /set-model gpt-4o-mini")
                return

            model = args[0]
            if model not in self._chat_bot.models():
                msg.user.send(f"目前仅支持: {self._chat_bot.models()}")
                return
            self._chat_bot.set_ai_model(model)
            msg.user.send(f"已设置模型为: {model}")
            return

        if cmd == "set-x":
            if len(args) == 0:
                msg.user.send("请输入数字. 例如: /set-x 10")
                return

            x = int(args[0])
            self._chat_bot.set_memory_size(x)
            msg.user.send(f"已设置聊天上下文的保持长度为: {x}")
            return

        if cmd == "debug":
            msg.user.send(
                f"""
AI服务:  OpenAI 
模型:    {self._chat_bot.get_ai_model()}
系统预设: {self._chat_bot.get_ai_prompt()}

上下文最大长度: {self._chat_bot.get_memory_size()}
上下文长度: {len(self._chat_bot.messages())}
上下文摘要: {[m.content[:10] + "..." for m in self._chat_bot.messages()]}

启动时间: {self._run_at.strftime("%Y-%m-%d %H:%M:%S")} 
运行时间: {self.run_time_str()} 
操作系统: {os.name} {platform.system()} {platform.release()} {platform.version()} {platform.machine()} {platform.processor()}
Python: {platform.python_version()}
"""
            )

        msg.user.send("未知命令. 请助输入 /help 查看帮助")

    def _on_message_received(self, msg):
        if msg.type == "Text":
            text = msg.text
            if text.strip().startswith("/"):
                _split = text.strip()[1:].split(" ")
                cmd = _split[0]
                args = _split[1:]
                self.on_receive_command(msg, cmd, args)
                return

            self.on_receive_user_text(msg)

        if msg.type == "Picture":
            self.on_receive_user_image(msg)
