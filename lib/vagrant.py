import vagrant


class Gateway:
    def __init__(self, vagrantfile):
        self.vagrant = vagrant.Vagrant(vagrantfile, quiet_stdout=False)

    def create(self):
        self.vagrant.up()

    def destroy(self):
        self.vagrant.destroy()
