FROM python:3.7
COPY ./scs /scs
# 设置工作目录
WORKDIR /scs

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 启动应用程序
CMD python main.py