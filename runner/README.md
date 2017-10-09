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
1.  Run the Flask application.
    ```
    python app.py
    ```
