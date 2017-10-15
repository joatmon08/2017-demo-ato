import os
from lib import container

ANSIBLE_RUNNER_IMAGE = 'ansible-runner:latest'

ANSIBLE_RUNNER_MOUNTS = {
    'ovs-vagrant/ssh-config': {
        'bind': '/root/.ssh/config',
        'mode': 'rw'
    },
    'ovs-vagrant/.vagrant/machines': {
        'bind': '/root/ovs-vagrant/.vagrant/machines',
        'mode': 'rw'
    },
    'playbook': {
        'bind': '/runner/playbook',
        'mode': 'rw'
    }
}

ANSIBLE_RUNNER_PORTS = {'8080/tcp': 8080}

ANSIBLE_RUNNER_ENVIRONMENT = {
    'APP_PLAYBOOK_PATH':'playbook',
    'APP_PLAYBOOK_NAME':'site.yml'
}

class Ansible:
    def __init__(self):
        self.client = container.Client()
        self.container = None

    @staticmethod
    def _get_absolute_path(path):
        return os.path.abspath(path)

    def create(self):
        mounts = {}
        for host_path, config in ANSIBLE_RUNNER_MOUNTS.items():
            mounts[self._get_absolute_path(host_path)] = config
        self.container = self.client.create_container(ANSIBLE_RUNNER_IMAGE, \
            volumes=mounts, ports=ANSIBLE_RUNNER_PORTS, \
            environment=ANSIBLE_RUNNER_ENVIRONMENT)

    def delete(self):
        self.client.destroy_container(self.container)
