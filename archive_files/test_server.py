from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
import flask
from openpyxl import load_workbook

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flask.flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flask.flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            take_mm(filename)
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>upload</title>
    <h1>upload</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
def take_mm(filename):
    wb = load_workbook(filename=filename)
    for obj in wb:
        id = obj

app.run()