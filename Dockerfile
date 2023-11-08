FROM python:3.12-alpine3.18

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /src

COPY /src /src

CMD ["python", "app.py"]