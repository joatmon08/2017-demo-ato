import time

class TestContainer:
    def __init__(self, client, ip_address, network_name):
        self.client = client
        self.container = self.client.create_container('busybox')
        self.client.set_network(network_name)
        self.ip_address = ip_address
        self.client.connect_container(self.container, self.ip_address)

    def ping(self, target):
        return self.client.execute_command(self.container, "ping -c 3 {0}".format(target))

    def destroy(self):
        self.client.destroy_container(self.container)

def _get_ip_addresses(cidr_block, start_num, num_ips):
    block = cidr_block.split('/')
    prefix = block[0].rsplit('.', 1)[0]
    ip_addresses = []
    for i in range(start_num, start_num + num_ips):
        ip_addresses.append("{0}.{1}".format(prefix, i))
    return ip_addresses


def _lost_packets(output):
    if '0 packets received' in str(output):
        return True
    return False


def run(host1_client, host2_client, network_name, cidr_block):
    ip_addresses = _get_ip_addresses(cidr_block, 5, 2)
    container1 = TestContainer(host1_client, ip_addresses[0], network_name)
    container2 = TestContainer(host2_client, ip_addresses[1], network_name)
    time.sleep(5)
    output1 = container1.ping(container2.ip_address)
    output2 = container2.ping(container1.ip_address)
    container1.destroy()
    container2.destroy()
    assert _lost_packets(output1) is False, 'Container on host1 cannot reach container on host2'
    assert _lost_packets(output2) is False, 'Container on host2 cannot reach container on host1'
