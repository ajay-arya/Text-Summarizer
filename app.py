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
    file = request.files['inputFile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        # convertFile(filename)
        return "jsonify({file: 'OK'})"
    else:
        return 'Opps!!, something went wrong.'


@app.route('/getSummary')
def summarizedFile():
    optimizedFile = './files/summ.txt'
    summary = generateSummary(optimizedFile, 4)
    return summary
    # return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
