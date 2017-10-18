import os

class UnitTest:
    def __init__(self, hosts_file):
        self.hosts_file = hosts_file

    def write_to_hosts_file(self, ssh_config):
        line = '{0} ansible_port={1} ansible_host={2} ansible_user={3} ansible_ssh_private_key_file={4}'.format(ssh_config.host, \
            ssh_config.port, ssh_config.hostname, ssh_config.user, \
            ssh_config.identity_file)
        f = open(self.hosts_file, 'w')
        f.write('[switches]\n')
        f.write('{0}\n'.format(line))
        f.close()

    def remove_hosts_file(self):
        os.remove(self.hosts_file)
