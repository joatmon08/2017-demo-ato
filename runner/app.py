from playbook import AnsiblePlaybook, AnsiblePlaybookNotFound, AnsiblePlaybookError
from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
try:
    app.config['APP_PORT'] = os.getenv('APP_PORT', 8080)
    app.config['APP_PLAYBOOK_PATH'] = os.getenv('APP_PLAYBOOK_PATH', 'playbook')
    app.config['APP_PLAYBOOK_NAME'] = os.getenv('APP_PLAYBOOK_NAME', 'site.yml')
except Exception as e:
    logging.error(e)


@app.errorhandler(AnsiblePlaybookNotFound)
def not_found_handler(error):
    return error.message, 404


@app.errorhandler(AnsiblePlaybookError)
def ansible_playbook_error_handler(error):
    return error, 500


@app.route('/')
def index():
    return jsonify({'status': 'healthy'})


@app.route('/runner/play', methods=['POST'])
def play():
    extra_vars = request.json
    playbook = AnsiblePlaybook(app.config['APP_PLAYBOOK_PATH'], app.config['APP_PLAYBOOK_NAME'])
    for key, var in extra_vars.items():
        playbook.add_extra_vars(key, var)
    return_code = playbook.execute()
    return jsonify({'playbook_return_code': str(return_code)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['APP_PORT'], debug=True)
