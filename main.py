import logging
import os
import utils
from flask import Flask, render_template, request, url_for

from utils import requires_auth

app = Flask(__name__)

@app.route('/')
@app.route('/landing_page')
@requires_auth
def landing_page():
    user = utils.get_user_from_db(request.authorization.username)
    if request.authorization.username == "admin" or user.type == "Admin":
        return show_registers()
    else:
        return show_entrys(user.defaultRegisterId)

@app.route('/show_registers')
@requires_auth
def show_registers():
    registers = utils.get_registers_from_db()
    if registers is None or len(registers) < 1:
        register = utils.register_factory("SingletonRegister")
        registers.append(register)
    user = utils.get_user_from_db(request.authorization.username)

    return render_template(
        'registers.html',
        user = user,
        registers= registers)

@app.route('/create_register')
@requires_auth
def create_register():
    users = utils.get_users_from_db(None)
    return render_template(
        'register_form.html',
        users=users)

@app.route('/update_register/<registerId>')
@requires_auth
def update_register(registerId):
    users = utils.get_users_from_db(None)
    register = utils.get_register_from_db(registerId)
    requirements = register.requirements
    userlist = []
    for user in register.users:
        userlist.append(user.identity)
    return render_template(
        'register_form.html',
        register=register,
        userlist = userlist,
        requirements=requirements,
        users=users)

@app.route('/submitted_register', methods=['POST'])
@requires_auth
def submitted_register():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    registerId = request.form.get('registerId')
    userIds = request.form.getlist('userIds[]')
    requirements = request.form.get('requirements')
    print "regis: " + str(registerId) + ", users: " + str(userIds) + ", reqs: " + str(requirements)
    utils.create_register(registerId, userIds, requirements)
    return render_template(
        'submitted_register.html',
        registerId=registerId,
        userIds = userIds,
        requirements = requirements)

@app.route('/show_register/<registerId>')
@requires_auth
def show_register(registerId):
    register = utils.register_factory(registerId)
    user = None
    return render_template(
       'register.html',
        user = user,
        register= register)

    # return error

@app.route('/show_entry_given_user/<userId>')
@requires_auth
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
@requires_auth
def form_entry(registerId):
    register = utils.register_factory(registerId)
    reqs = register.requirements
    return render_template(
        'table.html',
        users = register.users,
        items=reqs,
        registerId=registerId)

@app.route('/show_entrys/<registerId>')
@requires_auth
def show_entrys(registerId):
    entrys = utils.get_entrys_from_db(registerId)
    user = None

    return render_template(
        'entrys.html',
        registerId = registerId,
        user= user,
        entrys= entrys)

@app.route('/show_users/<registerId>')
@requires_auth
def show_users(registerId):
    users = utils.get_users_from_db(registerId)
    user = None

    return render_template(
        'users.html',
        user= user,
        users= users,
        registerId = registerId)

@app.route('/submitted_entry/<registerId>', methods=['POST'])
@requires_auth
def submitted_entry(registerId):
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.form.get('userId')
    cbname = request.form
    requirements_input = []
    for key in cbname:
        if key != 'userId':
            requirements_input.append(key)
    utils.store_entry(registerId, userId, requirements_input)
    return render_template(
        'submitted_table.html',
        registerId=registerId,
        userId = userId,
        cbname = requirements_input)

@app.route('/create_user')
@requires_auth
def create_user():
    return render_template(
        'user.html')

@app.route('/edit_user/<identity>')
@requires_auth
def edit_user(identity):
    user = utils.get_user_from_db(identity)
    return render_template(
        'user.html',
        user=user)

@app.route('/submitted_user', methods=['POST'])
@requires_auth
def submitted_user():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.form.get('identity')
    email = request.form.get('email')
    type = request.form.get('type')
    password = request.form.get('password')
    utils.create_user(userId, email)
    return render_template(
        'submitted_user.html',
        userId = userId,
        email = email)

@app.route('/submitted_edit_users_register/<registerId>', methods=['POST'])
@requires_auth
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
@requires_auth
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
