import docker
from docker import types
import os


class Network:
    name = None
    ipam_pool = None
    network = None

    def __init__(self, host, port=2375):
        os.environ['DOCKER_HOST'] = 'http://{0}:{1}'.format(host, port)
        self.client = docker.from_env()

    def create(self, name, cidr):
        self.ipam_pool = types.IPAMPool(
            subnet=cidr
        )
        ipam_config = types.IPAMConfig(
            pool_configs=[self.ipam_pool]
        )
        self.network = self.client.networks.create(name, ipam=ipam_config)

    def destroy(self):
        self.network.remove()
