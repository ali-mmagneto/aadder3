FROM ubuntu:20.04


RUN mkdir /app
RUN chmod 777 /app
WORKDIR /app

RUN apt -qq update

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow


RUN apt -qq install -y git wget curl busybox  python3 ffmpeg mediainfo python3-pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash","start.sh"]
