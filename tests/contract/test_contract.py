import pytest
import requests
import json
import os
import _thread
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from lib import vagrant, container


CONTRACT_HOST_IP_ADDRESS = '192.168.205.9'

TEST_CAPTURE_PORT = 8080

TEST_FIXTURE_PATH = 'tests/contract/fixtures'
VAGRANTFILE = "{0}/{1}".format(os.getcwd(), TEST_FIXTURE_PATH)

CONTRACT_NETWORK_NAME = str(int(time.time()))

contract_box = vagrant.Gateway(vagrantfile=VAGRANTFILE)
contract_docker_client = container.Client(CONTRACT_HOST_IP_ADDRESS)
data = None

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        global data
        self._set_headers()
        data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')


def start_server():
    HTTPServer(('', TEST_CAPTURE_PORT), RequestHandler).serve_forever()


@pytest.fixture(autouse=True)
def setup_and_teardown():
    try:
        _thread.start_new_thread(start_server, ())
    except Exception as e:
        print(e)
    contract_box.create()
    yield
    contract_box.destroy()


def test_request():
    contract_docker_client.create_network(CONTRACT_NETWORK_NAME)
    time.sleep(3)
    expected_container_network_body = {'container_network': CONTRACT_NETWORK_NAME}
    assert json.dumps(expected_container_network_body) == data