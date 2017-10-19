import os
from lib import container

ANSIBLE_RUNNER_IMAGE = 'joatmon08/ansible-runner:latest'

ANSIBLE_RUNNER_PORTS = {'8080/tcp': 8080}

ANSIBLE_RUNNER_ENVIRONMENT = {
    'APP_PLAYBOOK_PATH':'playbook',
    'APP_PLAYBOOK_NAME':'site.yml'
}

class Ansible:
    def __init__(self):
        self.client = container.Client()
        self.container = None

    def create(self, mounts):
        self.container = self.client.create_container(ANSIBLE_RUNNER_IMAGE, \
            volumes=mounts, ports=ANSIBLE_RUNNER_PORTS, \
            environment=ANSIBLE_RUNNER_ENVIRONMENT)

    def delete(self):
        self.client.destroy_container(self.container)
