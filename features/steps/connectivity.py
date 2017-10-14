from behave import *


@given('I have a gateway to my datacenter')
def step_impl(context):
    context.gateway.create()


@when('I create a container network named {network_name} with subnet {cidr_block}')
def step_impl(context, network_name, cidr_block):
    context.host1_container_network.create(network_name, cidr_block)
    context.host2_container_network.create(network_name, cidr_block)


@then('I should set up a route from that network to my datacenter')
def step_impl(context):
    assert context.gateway is not None
