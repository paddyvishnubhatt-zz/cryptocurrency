import logging
import utils
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
import utils
from flask import Flask, render_template, request, url_for

from utils import requires_auth

app = Flask(__name__)

@app.route('/api/v1/about_page')
def about_page():
    return render_template(
        'about.html',
        current_user=request.authorization.username)

@app.route('/')
@app.route('/api/v1/landing_page')
@requires_auth
def landing_page():
    user = utils.get_user_from_db(request.authorization.username)
    if user.type == "Admin":
        return show_projects()
    elif user.type == "Superuser":
        return show_users(None)
    else:
        return entry(user.defaultProjectId, user.identity)

@app.route('/api/v1/show_projects')
@requires_auth
def show_projects():
    projects = utils.get_projects_from_db()
    if projects is None or len(projects) < 1:
        pass

    return render_template(
        'projects.html',
        current_user = request.authorization.username,
        projects= projects)

@app.route('/api/v1/update_project/<projectId>')
@requires_auth
def update_project(projectId):
    users = utils.get_users_from_db(None)
    if projectId is not None and projectId != "___CREATE___" :
        project = utils.get_project_from_db(projectId)
        requirements = project.requirements
        userlist = []
        for user in project.users:
            userlist.append(user.identity)
        return render_template(
            'project.html',
            current_user=request.authorization.username,
            project=project,
            userlist = userlist,
            requirements=requirements,
            users=users)
    else:
        return render_template(
            'project.html',
            current_user=request.authorization.username,
            users=users)

@app.route('/api/v1/submitted_project', methods=['POST'])
@requires_auth
def submitted_project():
    # Do not forget to bring in project from UI back here to store entry against it - until then
    # project is singleton
    projectId = request.form.get('projectId')
    userIds = set(request.form.getlist('userIds[]'))
    requirements = request.form.get('requirements')
    stripped_reqs = requirements
    department = request.form.get('department')
    group = request.form.get('group')
    description = request.form.get('description')
    print "project: " + str(projectId) + ", users: " + str(userIds) + ", reqs: " + str(stripped_reqs)
    utils.update_project(projectId, department, group, description, userIds, stripped_reqs)
    return show_projects()

@app.route('/api/v1/show_project/<projectId>')
@requires_auth
def show_project(projectId):
    project = utils.get_project_from_db(projectId)
    requirements = project.requirements
    userlist = []
    for user in project.users:
        userlist.append(user.identity)
    return render_template(
        'project.html',
        current_user = request.authorization.username,
        project=project,
        userlist=userlist,
        requirements=requirements,
        users=project.users)

    # return error

@app.route('/api/v1/entry/<projectId>/<userId>')
@requires_auth
def entry(projectId, userId):
    project = utils.get_project_from_db(projectId)
    if userId == "__CREATE__":
        return render_template(
            'entry.html',
            current_user=request.authorization.username,
            project=project)
    else:
        entry = utils.get_entry_from_db(projectId, userId)
        if entry:
            return render_template(
                'entry.html',
                current_user=userId,
                userId = userId,
                date=entry.date,
                project=project,
                requirements=entry.requirements)
        else:
            return render_template(
                'entry.html',
                current_user=userId,
                userId = userId,
                project=project)

@app.route('/api/v1/show_summary/<projectId>')
@requires_auth
def show_summary(projectId):
    entrys = utils.get_entrys_from_db(projectId)
    userId = request.authorization.username
    score_table = {}
    for entry in entrys:
        for weight_splits in entry.weights:
            req_weight = weight_splits.split(":")
            if req_weight[0] in score_table:
                score_table[req_weight[0]] = float(score_table[req_weight[0]]) + float(req_weight[1])
            else:
                score_table[req_weight[0]] = float(req_weight[1])
    sorted_score_table = sorted(score_table.items(), key=lambda x: x[1])
    return render_template(
        'summary.html',
        current_user=userId,
        projectId = projectId,
        userId = userId,
        scoretable=sorted_score_table,
        entrys= entrys)

@app.route('/api/v1/show_entrys/<projectId>')
@requires_auth
def show_entrys(projectId):
    entrys = utils.get_entrys_from_db(projectId)
    userId = request.authorization.username
    return render_template(
        'entrys.html',
        current_user=userId,
        projectId = projectId,
        userId = userId,
        entrys= entrys)

@app.route('/api/v1/submitted_entry/<projectId>', methods=['POST'])
@requires_auth
def submitted_entry(projectId):
    # Do not forget to bring in project from UI back here to store entry against it - until then
    # project is singleton
    userId = request.authorization.username
    requirements_output = request.form.get("requirements_output")
    weights = request.form.get("weights")
    cbname = request.form
    requirements_input = []
    for key in cbname:
        if key != 'userId' and key != 'submit':
            requirements_input.append(key)
    project = utils.get_project_from_db(projectId)
    print ("entry: " + str(projectId) + ", " + userId + ", " + str(requirements_input))
    ent = utils.update_entry(projectId, userId, requirements_input, requirements_output, weights)
    return render_template(
            'entry.html',
            current_user=userId,
            userId = userId,
            date = ent.date,
            project=project,
            requirements=requirements_input)

@app.route('/api/v1/show_users/<projectId>')
@requires_auth
def show_users(projectId):
    users = utils.get_users_from_db(projectId)
    return render_template(
        'users.html',
        current_user=request.authorization.username,
        users= users,
        projectId = projectId)

@app.route('/api/v1/update_user/<projectId>/<identity>')
@requires_auth
def update_user(projectId, identity):
    user = utils.get_user_from_db(identity)
    project = utils.get_project_from_db(projectId)
    if user is not None and identity != "___CREATE___" :
        return render_template(
            'user.html',
            current_user = request.authorization.username,
            projectId=projectId,
            user=user)
    else:
        if projectId and projectId !=  "__CREATE__":
            return render_template(
                'user.html',
                current_user=request.authorization.username,
                defaultPassword=project.defaultPassword,
                projectId=projectId)
        else:
            return render_template(
                'user.html',
                current_user=request.authorization.username)

@app.route('/api/v1/submitted_user', methods=['POST', 'GET'])
@requires_auth
def submitted_user():
    # Do not forget to bring in project from UI back here to store entry against it - until then
    # project is singleton
    if request.method == 'GET':
        from flask import Flask, redirect, url_for
        return redirect(url_for('landing_page'))
    userId = request.form.get('identity')
    if userId == "admin":
        return render_template(
            "entry_error.html",
            h1Message="User ID Error, Go back and re-enter",
            title="User Add Error",
            mesage=userId + " is a system user, Please go back and use another identity and submit")
    email = request.form.get('email')
    type = request.form.get('type')
    password = request.form.get('password')
    projectId = request.form.get('projectId')
    print "*** " + str(userId) + ", " + str(email) + ", " + str(type) + ", " + str(password) + ", "  + str(projectId)
    user = utils.update_user(userId, email, type, password,projectId)
    users = utils.get_users_from_db(projectId)
    return render_template(
            'users.html',
            current_user=request.authorization.username,
            users=users,
            projectId=projectId)

@app.route('/api/v1/delete_project/<projectId>', methods=['DELETE'])
@requires_auth
def delete_project(projectId):
    utils.delete_project_from_db(projectId)
    return "OK", 200

@app.route('/api/v1/delete_users', methods=['DELETE'])
@requires_auth
def delete_users():
    utils.delete_users_from_db()
    return "OK", 200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]