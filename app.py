from flask import Flask, render_template, request, redirect, flash, jsonify
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
# app = Flask(__name__)

# app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
# # app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

# CORS(app)

# cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hi')
def Index():
    return 'jasjkdhaksjdhk'
    # return jsonify({'text': 'OK'})

@app.route('/api/v1/test', methods=['POST'])
def test():
    try:
        # data = request.get_json()
        # temp = wiki_scrape(data['link'])
        return jsonify({'Status': 'Success!', 'recived': "temp['link']"})
    except Exception as e:
        return jsonify({'Status': 'fail', 'error': e})


# @app.route('/getSummary', methods=['POST'])
# def summarizedFile():
#     lines = 4
#     # data = request.get_json()
#     # lines = data['lines']
#     optimizedFile = './files/summ.txt'
#     summary = generateSummary(optimizedFile, lines)
#     return jsonify({'Status': 'Success!', 'Summary': summary})

# Scaping wiki page
@app.route('/api/v1/scrapeWiki', methods=['POST'])
def scraper():
    try:
        data = request.get_json()
        # scrapeText = wiki_scrape(data['link'])
        scrapeText = wiki_scrape(data['link'])
        return jsonify({'Status': 'Success!', 'recived': data['link'], 'scrapeText': scrapeText})
    except Exception as e:
        return jsonify({'Status': 'fail', 'error': e})

# Pdf File Upload and generate Summari
@app.route('/api/v1/upload', methods=['POST'])
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
@app.route('/api/v1/getPreprocessed', methods=['POST'])
def sendPreProcessed():
    try:
        global preProcessedData
        if (preProcessedData != ''):
            return json.dumps({'Status': 'success', 'preprocessed': preProcessedData})
        else:
            return json.dumps({'Status': 'fail', 'error': 'no data avilable'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# reseve range test
@app.route('/api/v1/ranges', methods=['POST'])
def rangess():
    try:
        global SumariFileName
        global preProcessedData
        SumariFileName = './uploadedFiles/mgessaysandreflections.pdf'
        data = request.get_json()
        print(data)
        # scrapeText = wiki_scrape(data['link'])
        # lines = convertFile(SumariFileName, data['line'])
        return json.dumps({'Status': 'success', 'recived': 'yes'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Accept total range
@app.route('/api/v1/range', methods=['POST'])
# @cross_origin()
def perProcessing():
    try:
        global SumariFileName
        global preProcessedData
        data = request.get_json()
        line = wiki_scrape(data['lines'])
        # line = request.data
        # preProcessedData = convertFile(SumariFileName, line)
        if summary == 'error':
            return json.dumps({'Status': 'fail', 'error': 'some error'})
        else:    
            return json.dumps({'Status': 'success', 'recived': 'yes'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

if __name__ == "__main__":
    app.run(debug=True)
