from flask import Flask, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os

from optimize import store, convertFile, optimizeWiki
from flask_cors import CORS, cross_origin
from wiki_scraper import wiki_scrape
import json

UPLOAD_FOLDER = 'uploadedFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])

SummaryFileName = ''
preProcessedData = ''
FinalSummary = ''
scrapeText = ''
 
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
        global scrapeText
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
        global SummaryFileName
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
            SummaryFileName = name
            # convertFile(name, line)
            return json.dumps({'Status': 'success', 'recived': 'yes'})
        else:
            return json.dumps({'Status': 'fail', 'error': 'unknown'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Send PerProcessed data
@app.route('/api/v1/getDetails', methods=['POST'])
def sendPreProcessed():
    try:
        global preProcessedData
        global FinalSummary
        if (preProcessedData != ''):
            return json.dumps({'Status': 'success', 'preprocessed': preProcessedData, 'summary': FinalSummary})
        else:
            return json.dumps({'Status': 'fail', 'error': 'no data avilable'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

@app.route('/api/v1/wikiRange', methods=['POST'])
def rangess():
    try:
        data = request.get_json()
        print(data)
        # print(data['line'])
        # scrapeText = data['data']
        # temp = StoreText(scrapeText, data['line'])
        # preProcessedData = temp[0]
        # FinalSummary = temp[1]
        return json.dumps({'Status': 'success', 'preprocessed': 'preProcessedData', 'summary': 'FinalSummary'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Accept total range
@app.route('/api/v1/range', methods=['POST'])
def ranges():
    try:
        global SummaryFileName
        global preProcessedData
        global scrapeText
        global FinalSummary
        # SummaryFileName = './uploadedFiles/Animals.pdf'
        data = request.get_json()
        print(data)
        if data['wiki'] == 'no':
            print('pdf')
            temp = convertFile(SummaryFileName, data['line'])
        else:
            print('url')
            temp = optimizeWiki(scrapeText, data['line'])            
        preProcessedData = temp[0]
        FinalSummary = temp[1]
        return json.dumps({'Status': 'success', 'preprocessed': preProcessedData, 'summary': FinalSummary})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

# Wiki sumary
@app.route('/api/v1/sumarizeWiki', methods=['POST'])
def sumarizeWiki():
    try:
        global preProcessedData
        global FinalSummary
        data = request.get_json()
        temp = StoreText(data['data'])
        preProcessedData = temp[0]
        FinalSummary = temp[1]
        if (preProcessedData != ''):
            return json.dumps({'Status': 'success', 'preprocessed': preProcessedData, 'summary': FinalSummary})
        else:
            return json.dumps({'Status': 'fail', 'error': 'no data avilable'})
    except Exception as e:
        return json.dumps({'Status': 'fail', 'error': e})

if __name__ == "__main__":
    app.run(debug=True)
