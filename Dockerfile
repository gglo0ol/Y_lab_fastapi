FROM python:3.10-slim

WORKDIR /fastapi_app

COPY ./requirements.txt /fastapi_app/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /fastapi_app/requirements.txt

COPY . /fastapi_app
COPY ./schema /fastapi_app/schema

CMD ["python", "main.py"]