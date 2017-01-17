import logging
import os
import utils
from flask import Flask, render_template, request, url_for
from register import DEFAULT_REGISTER_NAME
from register import register_key


app = Flask(__name__)

@app.route('/')
@app.route('/show_registers')
def show_registers():
    registers = utils.get_registers_from_db()
    if registers is None or len(registers) < 1:
        register = utils.register_factory("SingletonRegister")
        registers.append(register)
    user = None

    return render_template(
        'registers.html',
        user = user,
        registers= registers)

@app.route('/create_register')
def create_register():
    users = utils.get_users_from_db(None)
    return render_template(
        'register_form.html',
        users=users)

@app.route('/submitted_register', methods=['POST'])
def submitted_register():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    registerId = request.form.get('registerId')
    userIds = request.form.getlist('userIds[]')
    requirements = request.form.getlist('requirements[]')
    print "regis: " + str(registerId) + ", users: " + str(userIds) + ", reqs: " + str(requirements)
    utils.create_register(registerId, userIds, requirements)
    return render_template(
        'submitted_register.html',
        registerId=registerId,
        userIds = userIds,
        requirements = requirements)

@app.route('/show_register/<registerId>')
def show_register(registerId):
    register = utils.register_factory(registerId)
    user = None
    return render_template(
       'register.html',
        user = user,
        register= register)

    # return error

@app.route('/show_entry_given_date/<date>')
def show_entry_given_date(date):
    entry = utils.get_entry_from_db_given_date(date)
    if entry is None:
        return
    user = None
    return render_template(
       'entry.html',
        user = user,
        entry= entry)

    # return error

@app.route('/show_entry_given_user/<userId>')
def show_entry_given_user(userId):
    entry = utils.get_entry_from_db_given_user(userId)
    if entry is None:
        return
    user = userId
    return render_template(
       'entry.html',
        user = userId,
        entry= entry)

    # return error

@app.route('/form_entry/<registerId>')
def form_entry(registerId):
    register = utils.register_factory(registerId)
    reqs = register.requirements
    return render_template(
        'table.html',
        users = register.users,
        items=reqs,
        registerId=registerId)

@app.route('/show_entrys/<registerId>')
def show_entrys(registerId):
    entrys = utils.get_entrys_from_db(registerId)
    user = None

    return render_template(
        'entrys.html',
        registerId = registerId,
        user= user,
        entrys= entrys)

@app.route('/show_users/<registerId>')
def show_users(registerId):
    users = utils.get_users_from_db(registerId)
    user = None

    return render_template(
        'users.html',
        user= user,
        users= users,
        registerId = registerId)

@app.route('/submitted_entry/<registerId>', methods=['POST'])
def submitted_entry(registerId):
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.form.get('userId')
    cbname = request.form
    utils.store_entry(registerId, userId, cbname)
    return render_template(
        'submitted_table.html',
        registerId=registerId,
        userId = userId,
        cbname = cbname)

@app.route('/create_user')
def create_user():
    return render_template(
        'user.html')

@app.route('/submitted_user', methods=['POST'])
def submitted_user():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.form.get('identity')
    email = request.form.get('email')
    utils.create_user(userId, email)
    return render_template(
        'submitted_user.html',
        userId = userId,
        email = email)

@app.route('/submitted_edit_users_register/<registerId>', methods=['POST'])
def submitted_edit_users_register(registerId):
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userIds = request.form.getlist('userIds[]')
    register = utils.get_register_from_db(registerId)
    utils.update_users_register(registerId, userIds)
    return render_template(
        'submitted_register.html',
        registerId=registerId,
        userIds=userIds,
        requirements=register.requirements)

@app.route('/edit_users/<registerId>')
def edit_users(registerId):
    register = utils.get_register_from_db(registerId)
    users = utils.get_users_from_db(None)
    return render_template(
        'edit_users.html',
        users = users,
        registerId=registerId)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
