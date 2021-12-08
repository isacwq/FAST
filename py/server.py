from flask import Flask, request, render_template
import lsh, competitors, fast, prioritize, scalability
import sys
import math
import os
import io

template_dir = os.path.abspath('..\\templates\\')
print(template_dir)
app = Flask('FAST')
print(app.template_folder)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('main_form.html')

@app.route('/prioritize', methods = ['POST'])
def funcionalidade_pagina():
    prog_v =  request.form['subject']
    entity = request.form['entity']
    algname = request.form['algorithm']
    repeats = int(request.form['repetitions'])

    prog, v = prog_v.split("_")

    directory = "output/{}_{}/".format(prog, v)
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory += "prioritized/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # FAST parameters
    k, n, r, b = 5, 10, 1, 10

    # FAST-f sample size
    if algname == "FAST-all":
        def all_(x): return x
        selsize = all_
    elif algname == "FAST-sqrt":
        def sqrt_(x): return int(math.sqrt(x)) + 1
        selsize = sqrt_
    elif algname == "FAST-log":
        def log_(x): return int(math.log(x, 2)) + 1
        selsize = log_
    elif algname == "FAST-one":
        def one_(x): return 1
        selsize = one_
    else:
        def pw(x): pass
        selsize = pw
    
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    if entity == "bbox":
        prioritize.bboxPrioritization(algname, prog, v, entity, k, n, r, b, repeats, selsize)
    else:
        prioritize.wboxPrioritization(algname, prog, v, entity, n, r, b, repeats, selsize)

    output = sys.stdout.getvalue()
    sys.stdout = stdout

    return output 

if __name__ == '__main__':
    port = 3000 if len(sys.argv) < 2 else int(sys.argv[1])
    app.run('localhost', port)