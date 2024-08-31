FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN  pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /code/src

CMD ["fastapi", "run", "src/", "--port", "8080"]
