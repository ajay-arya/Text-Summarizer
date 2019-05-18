from flask import Flask, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os

from optimize import store, convertFile
from summarize_old import generateSummary
from flask_cors import CORS, cross_origin
from wiki_scraper import wiki_scrape
import json

UPLOAD_FOLDER = 'uploadedFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
SumariFileName = ''

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def Index():
    return jsonify({'text': 'OK'})


# @app.route('/getSummary', methods=['POST'])
# def summarizedFile():
#     lines = 4
#     # data = request.get_json()
#     # lines = data['lines']
#     optimizedFile = './files/summ.txt'
#     summary = generateSummary(optimizedFile, lines)
#     return jsonify({'Status': 'Success!', 'Summary': summary})

# Scaping wiki page
@app.route('/api/scrapeWiki', methods=['POST'])
def scraper():
    try:
        data = request.get_json()
        scrapeText = wiki_scrape(data['link'])
        return jsonify({'Status': 'Success!', 'recived': data['link'], 'scrapeText': scrapeText})
    except Exception as e:
        return jsonify({'Status': 'fail', 'error': e})

# Pdf File Upload and generate Summari
@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        file = request.files['inputFile']
        # line = request.data['lines']
        line = 4
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            name = './uploadedFiles/' + filename
            # convertFile(name, line)
            return json.dumps({'Status': 'Success!', 'recived': 'yes'})
        else:
            return 'Opps!!, something went wrong.'
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="88")
