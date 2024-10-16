#!/bin/bash

local() {
    # 构建镜像
    docker build -t wechatbot .
}

# 定义函数用于构建 amd64 架构的 Docker 镜像
amd64() {
    # 构建镜像
    docker build --platform linux/amd64 -t wechatbot .
}