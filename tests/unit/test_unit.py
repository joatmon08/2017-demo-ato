import os
import pytest
from lib import vagrant, config, playbook

TEST_FIXTURE_PATH = 'tests/unit/fixtures'
HOSTS_FILE = "{0}/hosts".format(TEST_FIXTURE_PATH)
VAGRANTFILE = "{0}/{1}".format(os.getcwd(), TEST_FIXTURE_PATH)
unit_box = vagrant.Gateway(vagrantfile=VAGRANTFILE)
unit_test_config = config.UnitTest(HOSTS_FILE)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    unit_box.create()
    unit_test_config.write_to_hosts_file(unit_box.ssh_config())
    yield
    unit_test_config.remove_hosts_file()
    unit_box.destroy()

def test_check_openvswitch_playbook():
    unit_playbook = playbook.AnsiblePlaybook('playbook', 'site.yml', HOSTS_FILE)
    unit_playbook.add_extra_vars('container_network', 'test')
    assert unit_playbook.execute() == 0
