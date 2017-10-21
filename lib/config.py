import os
import re

class IntegrationTest:
    CONTAINER_ROOT_VAGRANT = '/root/ovs-vagrant'

    def __init__(self, vagrant_box):
        self.vagrant_box = vagrant_box
        self.vagrantfile = self.vagrant_box.vagrantfile
        self.ssh_config_file = "{0}/ssh-config".format(self.vagrantfile)
        self.mounts = None

    def _get_ssh_path(self):
        raw_ssh_config = self.vagrant_box.raw_ssh_config()
        groups = re.compile(r"IdentityFile (.*)/\.vagrant").search(raw_ssh_config).groups()
        return groups[0]

    @staticmethod
    def _get_absolute_path(path):
        python_path = os.environ['PYTHONPATH'].split(os.pathsep)[0]
        return os.path.abspath("{0}/{1}".format(python_path, path))

    def get_mounts(self):
        mounts = {}
        mounts[self.ssh_config_file] = {
            'bind': '/root/.ssh/config',
            'mode': 'rw'
        }
        mounts["{0}/.vagrant.d".format(self._get_ssh_path())] = {
            'bind': '/root/ovs-vagrant/.vagrant.d',
            'mode': 'rw'
        }
        mounts[self._get_absolute_path('playbook')] = {
            'bind': '/runner/playbook',
            'mode': 'rw'
        }
        return mounts

class UnitTest:
    def __init__(self, hosts_file):
        self.hosts_file = hosts_file

    def write_to_hosts_file(self, ssh_config):
        line = "{0} ansible_port={1} ansible_host={2} ansible_user={3} ansible_ssh_private_key_file={4}".format(
            ssh_config.host,
            ssh_config.port,
            ssh_config.hostname,
            ssh_config.user,
            ssh_config.identity_file)
        f = open(self.hosts_file, 'w')
        f.write('[switches]\n')
        f.write('{0}\n'.format(line))
        f.close()

    def remove_hosts_file(self):
        os.remove(self.hosts_file)
