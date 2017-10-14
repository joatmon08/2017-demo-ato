from behave import *
import smoke


@given('I have a gateway to my datacenter')
def step_impl(context):
    context.gateway.create()


@when('I create a container network named {network_name} with subnet {cidr_block}')
def step_impl(context, network_name, cidr_block):
    context.network_name = network_name
    context.cidr_block = cidr_block
    context.host1_client.create_network(context.network_name, cidr_block)
    context.host2_client.create_network(context.network_name, cidr_block)


@then('I should set up a route from that network to my datacenter')
def step_impl(context):
    smoke.run(context.host1_client, context.host2_client, context.network_name, context.cidr_block)
