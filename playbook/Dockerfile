FROM python:3

RUN pip install ansible

COPY . /playbook

WORKDIR /playbook

ENTRYPOINT ansible-playbook