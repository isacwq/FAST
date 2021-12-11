import io
import math
import os, shutil
import pathlib
import sys

from flask import Flask, jsonify, render_template, request, safe_join, send_file
from flask_cors import CORS

import prioritize

app = Flask(__name__)

# CORS CONFIG
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)

# APP CONFIG
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['ROOT_FOLDER'] = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = f'{app.config["ROOT_FOLDER"]}/uploads'
app.config['SUITE_FOLDER'] = f'{app.config["UPLOAD_FOLDER"]}/prioritized'
app.config['SUITE_FILE'] = 'FASTPrioritizedSuite.java'


def delete_folder_content(folder: pathlib.Path) -> None:
    """
    Deletes the content of the given folder.
    """
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as exception:
            print(f'Failed to delete {file_path}. Reason: {exception}')

def setup_folder(folder: pathlib.Path) -> None:
    """
    Sets up the given folder.
    """
    if not os.path.isdir(folder):
        os.mkdir(folder)

    delete_folder_content(folder)

def setup_folders() -> None:
    """
    Sets up all project needed folders.
    """
    setup_folder(app.config['UPLOAD_FOLDER'])

setup_folders()


@app.route('/upload', methods=['POST'])
def upload_files():
    response_object = {'status': 'success'}
    files = request.files.getlist('file[]', None)
    setup_folder(app.config['UPLOAD_FOLDER'])
    for uploaded_file in files:
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
    response_object['message'] = 'Files successfully uploaded!'
    return jsonify(response_object)


@app.route('/fastprioritize', methods=['GET', 'POST'])
def submit_prioritize():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()

        entity = post_data.get('entity')
        algorithm_name = post_data.get('algorithm')
        repeats = post_data.get('repetitions')

        response_object['message'] = f'{entity}, {algorithm_name}, {repeats}'
        prioritize.run_prioritize(app.config['UPLOAD_FOLDER'], algorithm_name)
        
        safe_path = safe_join(app.config['SUITE_FOLDER'], app.config['SUITE_FILE'])
    return send_file(safe_path)


if __name__ == '__main__':
    port = 3000 if len(sys.argv) < 2 else int(sys.argv[1])
    app.run('localhost', port)
