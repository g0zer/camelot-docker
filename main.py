import traceback
import camelot
import tempfile
import pickle
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/extract', methods=['POST'])
def go_camelot():
    try:
        temporary_file = request.files['file']
        if temporary_file:
            temporary_named_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            temporary_named_file.write(temporary_file.read())
            tables = camelot.read_pdf(temporary_named_file.name, flavor='stream', strict=False, pages='1-6')
            for idx, t in enumerate(tables):
                print(t.df.to_string(), flush=True)
                print(t.parsing_report, flush=True)
                with open(f"{secure_filename(temporary_file.filename)}_{idx}.txt", "w") as f:
                    f.write(t.df.to_string())
                    f.write(str(t.parsing_report))

            temporary_named_file.close()
        return "done!", 200 # jsonify(tables), 200 
    except: 
        ex = traceback.format_exc()
        print(str(ex), flush=True)
        return str(ex), 500


# ref: https://camelot-py.readthedocs.io/en/master/index.html

