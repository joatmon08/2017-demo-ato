# Ansible Runner App

This is a simple application that runs a specific Ansible playbook.
It has one simple endpoint which takes extra variables and passes
them to the playbook in question.

## Install
1.  Install dependencies
    ```
    pip install -r requirements.txt
    ```
1.  Set environment variables. Below are defaults.
    ```
    APP_PORT=8080
    APP_PLAYBOOK_PATH=playbook
    APP_PLAYBOOK_NAME=site.yml
    ```

## Run
1.  Add the playbook to ansible-runner/ folder, which is default.
1.  Run the Flask application.
    ```
    python app.py
    ```

## Run in Docker
1.  Build the Docker image.
1.  If necessary, mount the SSH configuration so you can SSH to the
hosts. You may need to mount the private keys.
    ```
     docker run -d -p 8080:8080 -v ovs-vagrant/ssh-config:/root/.ssh/config -v ovs-vagrant/.vagrant/machines:/root/ovs-vagrant/.vagrant/machines ansible-runner:latest
    ```