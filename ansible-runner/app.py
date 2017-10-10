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


@app.route('/')
def index():
    return jsonify({'status': 'healthy'})


@app.route('/runner/play', methods=['POST'])
def play():
    playbook = AnsiblePlaybook(app.config['APP_PLAYBOOK_PATH'], app.config['APP_PLAYBOOK_NAME'])
    extra_vars = request.get_json()
    for key, var in extra_vars.items():
        playbook.add_extra_vars(key, var)
    try:
        return_code = playbook.execute()
    except AnsiblePlaybookNotFound as e:
        return jsonify({'message': e.message}), 404
    except AnsiblePlaybookError as e:
        return jsonify({'message': e.message}), 500
    return jsonify({'playbook_return_code': return_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['APP_PORT'], debug=True)
