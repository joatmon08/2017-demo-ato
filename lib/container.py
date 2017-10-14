import docker
from docker import types
import os

class Client:
    name = None
    ipam_pool = None
    network = None

    LOOP_COMMAND = '/bin/sh -c "while true; do echo hello world; sleep 1; done"'

    def __init__(self, host, port=2375):
        os.environ['DOCKER_HOST'] = 'http://{0}:{1}'.format(host, port)
        self.client = docker.from_env()
        self.network = None

    def create_network(self, name, cidr):
        self.ipam_pool = types.IPAMPool(
            subnet=cidr
        )
        ipam_config = types.IPAMConfig(
            pool_configs=[self.ipam_pool]
        )
        options = {
            'com.docker.network.bridge.name': name
        }
        self.network = self.client.networks.create(name, \
            options=options, ipam=ipam_config)

    def set_network(self, name):
        self.network = self.client.networks.list(names=[name])[0]

    def destroy_network(self):
        self.network.remove()

    def connect_container(self, container, ip_address):
        self.network.connect(container, ipv4_address=ip_address)

    def create_container(self, image, network='bridge'):
        return self.client.containers.run(image, self.LOOP_COMMAND, \
            detach=True, network=network)

    def inspect_container(self, container):
        return self.client.containers.get(container.id)

    def execute_command(self, container, command):
        return container.exec_run(command)

    def destroy_container(self, container):
        container.remove(force=True)
