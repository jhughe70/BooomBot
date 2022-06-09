FROM python:3.9-slim

WORKDIR /app

RUN apt install ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]