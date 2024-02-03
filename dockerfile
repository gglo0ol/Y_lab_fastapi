FROM python:3.10-slim

WORKDIR /app/application

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./application /app/application

COPY ./application/tests /app/application/tests

COPY ./application/pytest.ini /app/application/pytest.ini

CMD ["python", "main.py"]
