# 使用官方 Python 3.11 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的 /app 目录
COPY . /app

# 安装在 requirements.txt 中列出的必需的包
# slim 版本的 python 没有安装 gcc，需要手动安装
RUN apt-get update && apt-get upgrade -y && apt-get install gcc -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# 运行 app.py 时，容器启动
CMD ["python", "main.py"]