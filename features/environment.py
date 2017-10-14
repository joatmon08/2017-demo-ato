from lib import vagrant, container
import os

vagrantfile = '{0}/ovs-vagrant'.format(os.getcwd())


def before_scenario(context, scenario):
    context.gateway = vagrant.Gateway(vagrantfile=vagrantfile)
    context.host1_container_network = container.Network('192.168.205.10', port=2375)
    context.host2_container_network = container.Network('192.168.205.11', port=2375)


def after_scenario(context, scenario):
    print("")
