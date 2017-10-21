from lib import vagrant, container, runner, config
import os

VAGRANTFILE = "{0}/fixtures".format(os.getcwd())

def before_scenario(context, scenario):
    context.gateway = vagrant.Gateway(vagrantfile=VAGRANTFILE)
    context.host1_client = container.Client(host='192.168.205.10', port=2375)
    context.host2_client = container.Client(host='192.168.205.11', port=2375)
    context.test_config = config.IntegrationTest(context.gateway)
    context.ansible_runner = runner.Ansible()

def after_scenario(context, scenario):
    context.ansible_runner.delete()
    context.gateway.destroy()
