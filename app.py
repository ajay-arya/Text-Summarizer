from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from optimize import store

UPLOAD_FOLDER = 'uploadedFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # file = request.files['inputFile']

    # return file.filename
    file = request.files['inputFile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return file.filename
    else:
        return render_template('fail.html')

@app.route('/getSummary')
def summarizedFile():
    return store()


if __name__ == "__main__":
    app.run(debug=True)
