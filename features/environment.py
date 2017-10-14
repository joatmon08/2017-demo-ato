from lib import vagrant, container
import os

vagrantfile = '{0}/ovs-vagrant'.format(os.getcwd())


def before_scenario(context, scenario):
    context.gateway = vagrant.Gateway(vagrantfile=vagrantfile)
    context.host1_client = container.Client('192.168.205.10', port=2375)
    context.host2_client = container.Client('192.168.205.11', port=2375)


def after_scenario(context, scenario):
    print("")
