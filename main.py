import logging
import utils
from flask import Flask, render_template, request, url_for

from utils import requires_auth

app = Flask(__name__)

@app.route('/about_page')
def about_page():
    return render_template(
        'about.html',
        current_user=request.authorization.username)

@app.route('/')
@app.route('/landing_page')
@requires_auth
def landing_page():
    user = utils.get_user_from_db(request.authorization.username)
    if user.type == "Admin":
        return show_registers()
    elif user.type == "Superuser":
        return show_users(None)
    else:
        return entry(user.defaultRegisterId, user.identity)

@app.route('/show_registers')
@requires_auth
def show_registers():
    registers = utils.get_registers_from_db()
    if registers is None or len(registers) < 1:
        pass

    return render_template(
        'registers.html',
        current_user = request.authorization.username,
        registers= registers)

@app.route('/update_register/<registerId>')
@requires_auth
def update_register(registerId):
    users = utils.get_users_from_db(None)
    if registerId is not None and registerId != "___CREATE___" :
        register = utils.get_register_from_db(registerId)
        requirements = register.requirements
        userlist = []
        for user in register.users:
            userlist.append(user.identity)
        return render_template(
            'register.html',
            current_user=request.authorization.username,
            register=register,
            userlist = userlist,
            requirements=requirements,
            users=users)
    else:
        return render_template(
            'register.html',
            current_user=request.authorization.username,
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
    utils.update_register(registerId, department, group, description, userIds, requirements)
    return show_registers()

@app.route('/show_register/<registerId>')
@requires_auth
def show_register(registerId):
    register = utils.get_register_from_db(registerId)
    requirements = register.requirements
    userlist = []
    for user in register.users:
        userlist.append(user.identity)
    return render_template(
        'register.html',
        current_user = request.authorization.username,
        register=register,
        userlist=userlist,
        requirements=requirements,
        users=register.users)

    # return error

@app.route('/entry/<registerId>/<userId>')
@requires_auth
def entry(registerId, userId):
    register = utils.get_register_from_db(registerId)
    if userId == "__CREATE__":
        return render_template(
            'entry.html',
            current_user=request.authorization.username,
            register=register)
    else:
        return render_template(
            'entry.html',
            current_user=userId,
            userId = userId,
            register=register)

@app.route('/show_entrys/<registerId>')
@requires_auth
def show_entrys(registerId):
    entrys = utils.get_entrys_from_db(registerId)
    userId = request.authorization.username
    return render_template(
        'entrys.html',
        current_user=userId,
        registerId = registerId,
        userId = userId,
        entrys= entrys)

@app.route('/show_users/<registerId>')
@requires_auth
def show_users(registerId):
    users = utils.get_users_from_db(registerId)
    return render_template(
        'users.html',
        current_user=request.authorization.username,
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
    ent = utils.create_entry(registerId, userId, requirements_input)
    register = utils.get_register_from_db(registerId)
    return render_template(
            'entry.html',
            current_user=userId,
            userId = userId,
            date = ent.date,
            register=register)

@app.route('/update_user/<registerId>/<identity>')
@requires_auth
def update_user(registerId, identity):
    user = utils.get_user_from_db(identity)
    if user is not None and identity != "___CREATE___" :
        return render_template(
            'user.html',
            current_user = request.authorization.username,
            registerId=registerId,
            user=user)
    else:
        if registerId and registerId !=  "__CREATE__":
            return render_template(
                'user.html',
                current_user=request.authorization.username,
                registerId=registerId)
        else:
            return render_template(
                'user.html',
                current_user=request.authorization.username)

@app.route('/submitted_user', methods=['POST'])
@requires_auth
def submitted_user():
    # Do not forget to bring in register from UI back here to store entry against it - until then
    # register is singleton
    userId = request.form.get('identity')
    email = request.form.get('email')
    type = request.form.get('type')
    password = request.form.get('password')
    registerId = request.form.get('registerId')
    user = utils.update_user(userId, email, type, password,registerId)
    users = utils.get_users_from_db(registerId)
    return render_template(
        'users.html',
        current_user=request.authorization.username,
        users=users,
        registerId=registerId)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
