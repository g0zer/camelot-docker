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
        response = {}
        temporary_file = request.files['file']
        if temporary_file:
            temporary_named_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            temporary_named_file.write(temporary_file.read())
            tables = camelot.read_pdf(temporary_named_file.name, flavor='stream', strict=False, pages='all')
            for idx, t in enumerate(tables):
                print(t.df.to_string(), flush=True)
                print(t.parsing_report, flush=True)
                tbl_result = {"table": t.df.to_dict(), "page": t.page, "order": t.order, "parsing_report": t.parsing_report}
                response[f"{idx}"] = tbl_result

            temporary_named_file.close()
        return response, 200 # , 200 
    except: 
        ex = traceback.format_exc()
        print(str(ex), flush=True)
        return str(ex), 500


# ref: https://camelot-py.readthedocs.io/en/master/index.html

