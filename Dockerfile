FROM python:3.9.3-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "tetsujin.py" ]