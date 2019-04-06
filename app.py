from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    #    if request.method == 'POST':
    #       file = request.files['inputFile']
    #       f.save(secure_filename(f.filename))
    #       return render_template('sucess.html')
    file = request.files['inputFile']
    
    return file.filename


if __name__ == "__main__":
    app.run(debug=True)
