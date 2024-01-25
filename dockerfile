FROM python:3.10-slim

WORKDIR /application

COPY ./requirements.txt /application/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /application/requirements.txt

COPY ./application /application

CMD ["python", "main.py"]
