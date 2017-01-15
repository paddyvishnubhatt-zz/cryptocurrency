# [START app]
import logging
import flask
from flask import url_for
import json
import jinja2
import os

# [START imports]
from flask import Flask, render_template, request
# [END imports]

app = Flask(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# [START form]
@app.route('/requirements')
def requirements():
    requirements = get_requirements()
    return flask.jsonify(requirements)
# [END form]

def get_requirements():
    requirement_items = []
    requirement_items.append("size")
    requirement_items.append("cost")
    requirement_items.append("smartapps")
    requirements = {'requirements' : requirement_items}
    return requirements

# [START form]
@app.route('/form')
def form():
    reqs = get_requirements()['requirements']
    lreqs = []
    for req in reqs:
        lreqs.append(req)
    return render_template(
        'table.html',
        items=lreqs)
# [END form]

# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_table():
    # peel out the form content using the keys in / from form.html
    cbname = request.form
    print cbname
    # [END submitted]

    # Start DB create/upsert operations
    # END

    # [START render_template]
    return render_template(
        'submitted_table.html',
        cbname = cbname)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
