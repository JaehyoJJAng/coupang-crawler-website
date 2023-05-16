FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./ ./

RUN pip install --upgrade pip && pip install -r requirement/requirements.txt

EXPOSE 8080

CMD [ "python", "server.py"]
