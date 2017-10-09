FROM python:3.4-alpine

ADD . /runner

WORKDIR /runner

RUN pip install -r requirements.txt

CMD ["python", "app.py"]