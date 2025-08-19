FROM python:3.11-slim

# 安装Chrome浏览器
WORKDIR /cache
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y -f ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app
COPY . .

# 安装Python依赖
RUN pip install requests DrissionPage

# 创建启动脚本
RUN echo $'#!/bin/bash\n\
google-chrome --headless --disable-gpu --remote-debugging-port=9222 --no-sandbox > /dev/null 2>&1 &\n\
sleep 3  # 等待浏览器启动\n\
python -u helper.py\n\
' > start.sh && chmod +x start.sh

# 启动服务
CMD ["./start.sh"]
