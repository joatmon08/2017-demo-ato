FROM python:3.6

ADD . /runner

WORKDIR /runner

RUN pip install -r requirements.txt

CMD ["python", "app.py"]