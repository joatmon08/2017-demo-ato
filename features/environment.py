from lib import vagrant, container, runner
import os

VAGRANTFILE = '{0}/ovs-vagrant'.format(os.getcwd())

def before_scenario(context, scenario):
    context.gateway = vagrant.Gateway(vagrantfile=VAGRANTFILE)
    context.host1_client = container.Client(host='192.168.205.10', port=2375)
    context.host2_client = container.Client(host='192.168.205.11', port=2375)
    context.ansible_runner = runner.Ansible()
    context.ansible_runner.create()


def after_scenario(context, scenario):
    context.ansible_runner.delete()
    context.gateway.destroy()
