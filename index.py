
from pandas_profiling import ProfileReport
from flask import Flask, redirect, render_template, request, url_for, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

UPLOAD_FOLDER = 'static/uploads/'
DOWNLOADS_FOLDER = 'static/downloads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/carga", methods=['POST'])
def carga():
    csv = request.files['file']
    filename = secure_filename(csv.filename)

    ruta_upload = os.path.join(app.config['UPLOAD_FOLDER'] + filename)
    ruta_download = os.path.join(app.config['DOWNLOADS_FOLDER'] + filename[:-4] + ".html")

    csv.save(ruta_upload)

    df = pd.read_csv(ruta_upload)
    prof = ProfileReport(df)
    prof.to_file(output_file=ruta_download)

    os.remove(ruta_upload)
    #return redirect(url_for('index'))
    return send_file(ruta_download, download_name='output.html', as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


if __name__ == "__main__":
    app.run(debug=True)