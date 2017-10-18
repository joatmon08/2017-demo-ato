.PHONY: unit bootstrap

unit: check_ansible_syntax check_openvswitch_playbook

check_ansible_syntax: bootstrap
	sh -c '. venv/bin/activate; ansible-playbook playbook/site.yml -i playbook/hosts --syntax-check'

check_openvswitch_playbook: bootstrap
	sh -c '. venv/bin/activate; pytest --capture=no'

bootstrap: virtualenv
ifneq ($(wildcard requirements.txt),)
	venv/bin/pip install -r requirements.txt
endif
	make clean

virtualenv:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools
