from flask import Flask, request, render_template
from funcionalidade import funcionalidade_principal

app = Flask('')

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('main_form.html')

@app.route('/funcionalidade', methods = ['POST'])
def funcionalidade_pagina():
    print(request.form)
    nome =  request.form['nome']
    return funcionalidade_principal(nome)
app.run()