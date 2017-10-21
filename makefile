.PHONY: unit bootstrap

unit: check_ansible_syntax check_openvswitch_playbook

contract: bootstrap
	sh -c '. venv/bin/activate; pytest tests/contract --capture=no'

integration: bootstrap
	sh -c '. venv/bin/activate; cd tests/smoke && behave'

check_ansible_syntax: bootstrap
	sh -c '. venv/bin/activate; ansible-playbook playbook/site.yml -i playbook/hosts --syntax-check'

check_openvswitch_playbook: bootstrap
	sh -c '. venv/bin/activate; pytest tests/unit --capture=no'

openvswitch_box:
	cd ovs-vagrant && vagrant up
	cd ovs-vagrant && vagrant package --output openvswitch.box
	cd ovs-vagrant && vagrant box add openvswitch openvswitch.box --force

bootstrap: virtualenv
ifneq ($(wildcard requirements.txt),)
	venv/bin/pip install -r requirements.txt
endif

virtualenv:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools
