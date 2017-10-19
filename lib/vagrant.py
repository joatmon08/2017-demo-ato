import vagrant

class SSHConfig:
    host = 'unit'
    hostname = '127.0.0.1'
    user = 'vagrant'
    port = 2222
    identity_file = None

    def __init__(self, config):
        self.config = config
        self.parse()

    def parse(self):
        lines = self.config.splitlines()
        for line in lines:
            if 'Host ' in line:
                self.host = line.split()[1]
            if 'HostName ' in line:
                self.hostname = line.split()[1]
            if 'User ' in line:
                self.user = line.split()[1]
            if 'Port ' in line:
                self.port = line.split()[1]
            if 'IdentityFile ' in line:
                self.identity_file = line.split()[1]

class Gateway:

    def __init__(self, vagrantfile):
        self.vagrantfile = vagrantfile
        self.vagrant = vagrant.Vagrant(self.vagrantfile, quiet_stdout=False)

    def create(self):
        self.vagrant.up()

    def destroy(self):
        self.vagrant.destroy()

    def raw_ssh_config(self):
        return self.vagrant.ssh_config()

    def ssh_config(self):
        return SSHConfig(self.vagrant.ssh_config())
