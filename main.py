# [START app]
import logging
import json
import jinja2
import os
from datetime import datetime
from flask import Flask, render_template, request, url_for

from register import Entry
from register import Author
from register import Register

from register import DEFAULT_REGISTER_NAME
from register import register_key

from google.appengine.api import users

# [START imports]
# [END imports]

app = Flask(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/show_registers')
def show_registers():
    #START DB GET
    registers = get_registers_from_db()
    if registers is None or len(registers) < 1:
        register = register_factory("SingletonRegister")
        registers.append(register)
    user = users.get_current_user()

    if user:
        url = users.create_logout_url(request.url)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.url)
        url_linktext = 'Login'

    return render_template(
        'registers.html',
        user = user,
        registers= registers)

# [SHOW Register - Its a singleton for now, this will create a hard-coded register and persist if not already there]
# For Debugging only -
@app.route('/register_debug/<registerId>')
def register_debug(registerId):
    __register = get_register_from_db(registerId)
    requirement_items = __register.requirements
    requirements = {'requirements': requirement_items}
    return flask.jsonify(requirements)
# [END form]

@app.route('/show_register/<registerId>')
def show_register(registerId):
    register = register_factory(registerId)
    user = users.get_current_user()
    return render_template(
       'register.html',
        user = user,
        register= register)

    # return error

# [END form]

@app.route('/show_entry/<date>')
def show_entry(date):
    entry = get_entry_from_db(date)
    print "***** " + str(date) + ", " + str(entry)
    if entry is None:
        return
    user = users.get_current_user()
    return render_template(
       'entry.html',
        user = user,
        entry= entry)

    # return error

# [END form]

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_registers_from_db():
    register_name = request.args.get('register_name',
                                     DEFAULT_REGISTER_NAME)
    register_query = Register.query(
        ancestor=register_key(register_name))

    return register_query.fetch(100)

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_register_from_db(registerId):
    if registerId is None:
        registerId = "SingletonRegister"
    register_name = request.args.get('register_name',
                                     DEFAULT_REGISTER_NAME)
    register_query = Register.query(
        ancestor=register_key(register_name))

    for register in register_query:
        if register.registerId == registerId:
            return register

    return None

def get_entry_from_db(date):
    register_name = request.args.get('register_name',
                                     DEFAULT_REGISTER_NAME)
    entrys_query = Entry.query(
        ancestor=register_key(register_name)).order(-Entry.date)

    entrys = entrys_query.fetch(100)
    returnEntrys = []
    for entry in entrys:
        datestr = entry.date.strftime("%Y-%m-%d% %H:%M:%S.%f")
        print date + ", " + datestr
        if date == datestr:
            return entry

    return None

def get_entrys_from_db(registerId):
    register_name = request.args.get('register_name',
                                     DEFAULT_REGISTER_NAME)
    entrys_query = Entry.query(
        ancestor=register_key(register_name)).order(-Entry.date)

    entrys = entrys_query.fetch(100)
    returnEntrys = []
    for entry in entrys:
        if entry.register.registerId == registerId:
            returnEntrys.append(entry)

    return returnEntrys

def register_factory(registerId):
    # We know it is a singleton for now
    registerFromDB = get_register_from_db(registerId)
    if registerFromDB:
        return registerFromDB
    else:
        requirement_items = []
        requirement_items.append("size")
        requirement_items.append("cost")
        requirement_items.append("smartapps")
        register_name = request.args.get('register_name',
                                         DEFAULT_REGISTER_NAME)
        register = Register(parent=register_key(register_name))
        register.registerId = registerId
        register.requirements = requirement_items
        users = ["user1", "user2"]
        register.users = users
        register.put()
        return register

# [START form entry]
@app.route('/form_entry/<registerId>')
def form_entry(registerId):
    register = register_factory(registerId)
    reqs = register.requirements
    return render_template(
        'table.html',
        items=reqs)
# [END form]

# [Default landing page - shows existing entries if exists]
@app.route('/show_entrys/<registerId>')
def show_entrys(registerId):
    #START DB GET
    entrys = get_entrys_from_db(registerId)
    user = users.get_current_user()

    if user:
        url = users.create_logout_url(request.url)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.url)
        url_linktext = 'Login'

    print str(user) + ", " + str(entrys)

    return render_template(
        'entrys.html',
        user= user,
        entrys= entrys)

# [START submitted]
@app.route('/submitted_entry', methods=['POST'])
def submitted_table_entry():
    # peel out the form content using the keys in / from form.html
    cbname = request.form
    # [END submitted]

    # Start DB create/upsert operations
    register_name = request.args.get('register_name',
                                     DEFAULT_REGISTER_NAME)
    entry = Entry(parent=register_key(register_name))

    if users.get_current_user():
        entry.author = Author(
            identity=users.get_current_user().user_id(),
            email=users.get_current_user().email())

    entry.register = register_factory("SingletonRegister")
    requirements = []
    for key in cbname:
        requirements.append(key)
    entry.requirements = requirements
    entry.put()
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
