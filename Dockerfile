# 先下载一个可以运行flask的基础镜像
FROM tiangolo/uwsgi-nginx-flask:python3.6
# 设置作者信息
MAINTAINER Aasee<fxhaoo@163.com>
# 设置工作目录
WORKDIR /app
# 将当前目录下的所有文件复制到docker引擎中的工作目录
COPY ./ /app

USER root
# 安装依赖
RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口
EXPOSE 80
# 执行我们的脚本文件
CMD ["python3", "run.py","0.0.0.0","80"]
