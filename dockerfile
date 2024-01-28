FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./application /app/application

COPY ./tests /app/tests

CMD ["python", "main.py"]
