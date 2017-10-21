import os
import copy
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
import logging


class AnsiblePlaybookNotFound(Exception):
    def __init__(self, playbook_path=''):
        self.message = "playbook {0} does not exist".format(playbook_path)


class AnsiblePlaybookError(Exception):
    def __init__(self, message=""):
        self.message = message


class AnsiblePlaybook:

    def __init__(self, playbook_path, playbook, hosts_file, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.playbook_path = "{0}/{1}".format(playbook_path, playbook)
        if not os.path.exists(self.playbook_path):
            raise AnsiblePlaybookNotFound(self.playbook_path)
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=hosts_file)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.options = self._set_options()
        self.passwords = {}
        self.variable_manager.extra_vars = {
            'ansible_become_pass': 'vagrant'
        }

    @staticmethod
    def _set_options():
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
                                         'syntax', 'connection','module_path',
                                         'forks', 'remote_user', 'private_key_file',
                                         'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method',
                                         'become_user', 'verbosity', 'check', 'diff'])
        return Options(listtags=False, listtasks=False, listhosts=False,
                       syntax=False, connection='ssh', module_path=None,
                       forks=100, remote_user='vagrant', private_key_file=None,
                       ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                       scp_extra_args=None, become=True, become_method='sudo',
                       become_user='root', verbosity=0, check=False, diff=None)

    def add_extra_vars(self, key, value):
        extra_vars = copy.copy(self.variable_manager.extra_vars)
        extra_vars[key] = value
        self.variable_manager.extra_vars = extra_vars

    def execute(self):
        self.logger.info("executing playbook {0}".format(self.playbook_path))
        try:
            pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    options=self.options,
                                    passwords=self.passwords)
            return_code = pbex.run()
            if return_code != 0:
                raise AnsiblePlaybookError("ansible playbook returned error code {0}".format(return_code))
            return return_code
        except Exception as e:
            raise AnsiblePlaybookError(str(e))
