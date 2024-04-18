FROM python:3.10

ENV TZ=Asia/Tehran


RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev pkg-config && \
    apt-get clean

RUN mkdir /storage /app
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app
ADD . .

CMD ["bash", "./deployment/docker-entrypoint.sh"]
