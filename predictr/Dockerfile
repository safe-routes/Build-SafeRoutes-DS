FROM ubuntu:18.04

LABEL Kevin Brack "brackkevin@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python3"]

CMD ["app.py"]