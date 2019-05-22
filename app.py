from flask import Flask, render_template, request, redirect, flash, jsonify
# try:
#     from flask.ext.cors import CORS
# except ImportError:
#     import os
#     parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     os.sys.path.insert(0, parentdir)

#     from flask.ext.cors import CORS

from werkzeug.utils import secure_filename
import os

from optimize import store, convertFile
from flask_cors import CORS, cross_origin
from wiki_scraper import wiki_scrape
import json

UPLOAD_FOLDER = 'uploadedFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])

SumariFileName = ''
preProcessedData = ''
 
app = Flask(__name__)

app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
# app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

cors = CORS(app)

# cors = CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hi')
def Index():
    return 'jasjkdhaksjdhk'
    # return jsonify({'text': 'OK'})


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
        global SumariFileName
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
            SumariFileName = name
            print('***NAME***' + SumariFileName)
            # convertFile(name, line)
            return json.dumps({'Status': 'success', 'recived': 'yes'})
        else:
            return json.dumps({'Status': 'fail', 'error': 'unknown'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Send PerProcessed data
@app.route('/api/getPreprocessed', methods=['POST'])
def sendPreProcessed():
    try:
        global preProcessedData
        if (preProcessedData != ''):
            return json.dumps({'Status': 'success', 'preprocessed': preProcessedData})
        else:
            return json.dumps({'Status': 'fail', 'error': 'no data avilable'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Accept total range
@app.route('/api/range', methods=['POST'])
@cross_origin()
def perProcessing():
    try:
        global SumariFileName
        global preProcessedData
        # data = request.get_json()
        # line = wiki_scrape(data['range'])
        line = request.data
        preProcessedData = convertFile(SumariFileName, line)
        if summary == 'error':
            return json.dumps({'Status': 'fail', 'error': 'some error'})
        else:    
            return json.dumps({'Status': 'success', 'recived': 'yes'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

if __name__ == "__main__":
    app.run(debug=True)
