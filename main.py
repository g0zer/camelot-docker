import traceback
import camelot
import tempfile
import pickle

from flask import Flask, jsonify, request

app = Flask(__name__)




@app.route('/hi')
def hi():
    return jsonify("hello!")


@app.route('/extract', methods=['POST'])
def go_camelot():
    try:
        temporary_file = request.files['file']
        if temporary_file:
            temporary_named_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            temporary_named_file.write(temporary_file.read())
            tables = camelot.read_pdf(temporary_named_file.name, flavor='stream', strict=False, pages='1-6')

            for t in tables:
                print(t.df, flush=True)
                print(t.parsing_report, flush=True)
            temporary_named_file.close()
        return "done!", 200 # jsonify(tables), 200 
    except: 
        ex = traceback.format_exc()
        print(str(ex), flush=True)
        return str(ex), 500

@app.route('/camelottest', methods=['POST'])
def go_extract_table():
    try:
        tables = camelot.read_pdf('hlane_1.pdf', flavor='stream', strict=False, pages='1-6')
        for t in tables:
            print(t.df, flush=True)
            print(t.parsing_report, flush=True)

        return "done!", 200 # jsonify(tables), 200 
    except: 
        ex = traceback.format_exc()
        print(str(ex), flush=True)
        return str(ex), 500


# ref: https://camelot-py.readthedocs.io/en/master/index.html

