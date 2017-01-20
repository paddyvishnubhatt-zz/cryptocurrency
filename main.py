import logging
import os
import utils
from flask import Flask, render_template, request, url_for

from utils import requires_auth

app = Flask(__name__)

@app.route('/about_page')
def about_page():
    return render_template(
        'about.html')

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

@app.route('/update_register/<registerId>')
@requires_auth
def update_register(registerId):
    users = utils.get_users_from_db(None)
    print registerId
    if registerId is not None and registerId != "___CREATE___" :
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
    else:
        return render_template(
            'register_form.html',
            users=users)

@app.route('/submitted_register', methods=['POST'])
@requires_auth
def submitted_register():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    registerId = request.form.get('registerId')
    userIds = set(request.form.getlist('userIds[]'))
    requirements = request.form.get('requirements')
    department = request.form.get('department')
    group = request.form.get('group')
    description = request.form.get('description')
    print "regis: " + str(registerId) + ", users: " + str(userIds) + ", reqs: " + str(requirements)
    register = utils.update_register(registerId, department, group, description, userIds, requirements)
    return render_template(
        'register.html',
        register=register)

@app.route('/show_register/<registerId>')
@requires_auth
def show_register(registerId):
    register = utils.register_factory(registerId)
    return render_template(
       'register.html',
        register= register)

    # return error

@app.route('/show_entry_given_user/<registerId>/<userId>')
@requires_auth
def show_entry_given_user(registerId, userId):
    entry = utils.get_entry_from_db_given_user(registerId, userId)
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
        userId = request.authorization.username,
        items=reqs,
        registerId=registerId)

@app.route('/show_entrys/<registerId>')
@requires_auth
def show_entrys(registerId):
    entrys = utils.get_entrys_from_db(registerId)

    return render_template(
        'entrys.html',
        registerId = registerId,
        entrys= entrys)

@app.route('/show_users/<registerId>')
@requires_auth
def show_users(registerId):
    users = utils.get_users_from_db(registerId)
    return render_template(
        'users.html',
        users= users,
        registerId = registerId)

@app.route('/submitted_entry/<registerId>', methods=['POST'])
@requires_auth
def submitted_entry(registerId):
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.authorization.username
    cbname = request.form
    requirements_input = []
    for key in cbname:
        if key != 'userId':
            requirements_input.append(key)
    entry = utils.create_entry(registerId, userId, requirements_input)
    return render_template(
        'entry.html',
        user=userId,
        entry=entry)

@app.route('/update_user/<identity>')
@requires_auth
def update_user(identity):
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
    user = utils.update_user(userId, email, type, password)
    return render_template(
        'user.html',
        user=user)

@app.route('/submitted_edit_users_register/<registerId>', methods=['POST'])
@requires_auth
def submitted_edit_users_register(registerId):
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userIds = request.form.getlist('userIds[]')
    register = utils.get_register_from_db(registerId)
    register = utils.update_users_register(registerId, userIds)
    return render_template(
        'register.html',
        register=register)

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
