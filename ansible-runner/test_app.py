import requests
import json

url = 'http://127.0.0.1:8080'

headers = {
    'Content-Type': 'application/json'
}


def test_should_get_healthy_endpoint():
    r = requests.get(url)
    r.raise_for_status()
    assert r.json() == {'status': 'healthy'}


def test_should_successfully_run_openvswitch_playbook():
    data = json.dumps({})
    r = requests.post(url + '/runner/play', headers=headers, data=data)
    r.raise_for_status()
    assert r.json() == {'playbook_return_code': 0}


def test_should_fail_openvswitch_playbook():
    data = json.dumps({
        'container_network': 'not_a_network'
    })
    r = requests.post(url + '/runner/play', headers=headers, data=data)
    assert r.status_code == 500
    assert r.json() == {'message': 'ansible playbook returned error code 2'}
