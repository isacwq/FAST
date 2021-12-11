import io
import math
import os
import pathlib
import sys

from flask import Flask, jsonify, render_template, request
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


def delete_folder_content(folder: pathlib.Path) -> None:
    """
    Deletes the content of the given folder.
    """
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
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


        response_object['message'] = f'{prog_v}, {entity}, {algorithm_name}, {repeats}'
        # fast_prioritize(prog_v, entity, algorithm_name, repeats)
    return jsonify(response_object)


def fast_prioritize(prog_v, entity, algorithm_name, repeats):
    prog, v = prog_v.split('_')

    directory = f'output/{prog}_{v}/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory += "prioritized/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # FAST parameters
    k, n, r, b = 5, 10, 1, 10

    # FAST-f sample size
    if algorithm_name == 'FAST-all':
        def all_(x): return x
        selsize = all_
    elif algorithm_name == 'FAST-sqrt':
        def sqrt_(x): return int(math.sqrt(x)) + 1
        selsize = sqrt_
    elif algorithm_name == 'FAST-log':
        def log_(x): return int(math.log(x, 2)) + 1
        selsize = log_
    elif algorithm_name == 'FAST-one':
        def one_(x): return 1
        selsize = one_
    else:
        def pw(x): pass
        selsize = pw
    
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    if entity == "bbox":
        prioritize.bboxPrioritization(algorithm_name, prog, v, entity, k, n, r, b, repeats, selsize)
    else:
        prioritize.wboxPrioritization(algorithm_name, prog, v, entity, n, r, b, repeats, selsize)

    output = sys.stdout.getvalue()
    sys.stdout = stdout

    return output


if __name__ == '__main__':
    port = 3000 if len(sys.argv) < 2 else int(sys.argv[1])
    app.run('localhost', port)
