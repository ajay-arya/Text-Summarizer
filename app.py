from flask import Flask, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os
from optimize import store, convertFile
from summarize import generateSummary

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
    print(request)
    file = request.files['inputFile']
    # line = request.data['lines']
    line = 4
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        name = './uploadedFiles/' + filename
        convertFile(name, line)
        return "jsonify({file: 'OK'})"
    else:
        return 'Opps!!, something went wrong.'


# @app.route('/getSummary', methods=['POST'])
# def summarizedFile():
#     lines = 4
#     # data = request.get_json()
#     # lines = data['lines']
#     optimizedFile = './files/summ.txt'
#     summary = generateSummary(optimizedFile, lines)
#     return jsonify({'Status': 'Success!', 'Summary': summary})


if __name__ == "__main__":
    app.run(debug=True)
