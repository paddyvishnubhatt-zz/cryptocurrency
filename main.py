import logging
import utils
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
import utils
from flask import Flask, render_template, request, url_for, redirect
import datetime
from utils import requires_auth

app = Flask(__name__)

@app.route('/api/v1/about_page')
def about_page():
    return render_template(
        'about.html',
        current_user=request.authorization.username)

@app.route('/')
@requires_auth
def root_page():
    user = utils.get_user_from_db(request.authorization.username)
    if user.type == "Admin":
        return show_projects()
    elif user.type == "Superuser":
        return show_users(None)
    else:
        return show_entrys_given_user(user.identity)


@app.route('/api/v1/landing_page')
@requires_auth
def landing_page():
    return redirect(url_for('root_page'))

@app.route('/api/v1/show_projects')
@requires_auth
def show_projects():
    current_user = request.authorization.username
    user = utils.get_user_from_db(current_user)
    if user.type == 'User':
        return "Unauthorized", 404
    projects = utils.get_projects_from_db(current_user)
    if projects is None or len(projects) < 1:
        pass
    return render_template(
        'projects.html',
        current_user = current_user,
        projects= projects)

@app.route('/api/v1/show_project/<projectId>')
@requires_auth
def show_project(projectId):
    users = utils.get_users_from_db(None)
    if projectId is not None and projectId != "___CREATE___" :
        project = utils.get_project_from_db(projectId)
        requirements = project.requirements
        userlist = project.userIds
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

@app.route('/api/v1/submitted_project', methods=['POST', 'GET'])
@requires_auth
def submitted_project():
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    projectId = request.form.get('projectId')
    userIds = set(request.form.getlist('userIds[]'))
    requirements = request.form.get('requirements')
    due_date = request.form.get('due_date')
    stripped_reqs = requirements
    department = request.form.get('department')
    group = request.form.get('group')
    description = request.form.get('description')
    print "project: " + str(projectId) + ", users: " + str(userIds) + ", reqs: " + str(stripped_reqs)
    utils.update_project(projectId, department, group, description, userIds, stripped_reqs, due_date)
    return redirect(url_for('landing_page'))

@app.route('/api/v1/show_entry/<projectId>/<userId>')
@requires_auth
def show_entry(projectId, userId):
    project = utils.get_project_from_db(projectId)
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
    entrys = utils.get_entrys_from_given_project_db(projectId)
    userId = request.authorization.username
    score_table = {}
    length = 0
    weights = []
    for entry in entrys:
        if len(entry.requirements) > 0:
            length += 1
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
        length=length,
        entrys= entrys)

@app.route('/api/v1/show_entrys_given_project/<projectId>')
@requires_auth
def show_entrys_given_project(projectId):
    users = utils.get_users_from_db(projectId)
    entrys = []
    for user in users:
        entry = utils.get_entry_from_db(projectId, user.identity)
        if entry is None:
            entry = utils.get_entry_from_db(projectId, user.identity)
            if entry is None:
                entry = utils.update_entry(projectId, user.identity, None, None, None)
        entrys.append(entry)

    userId = request.authorization.username
    return render_template(
        'entrys.html',
        current_date=datetime.datetime.now(),
        current_user=userId,
        projectId = projectId,
        userId = userId,
        entrys= entrys)

@app.route('/api/v1/show_entrys_given_user/<userId>')
@requires_auth
def show_entrys_given_user(userId):
    entrys = []
    projects = utils.get_projects_from_db(userId)
    for project in projects:
        entry = utils.get_entry_from_db(project.projectId, userId)
        if entry is None:
            entry = utils.update_entry(project.projectId, userId, None, None, None)
        entrys.append(entry)
    return render_template(
        'entrys.html',
        current_date=datetime.datetime.now(),
        current_user=userId,
        userId = userId,
        entrys= entrys)

@app.route('/api/v1/submitted_entry/<projectId>', methods=['POST', 'GET'])
@requires_auth
def submitted_entry(projectId):
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    userId = request.authorization.username
    requirements_output = request.form.get("requirements_output")
    cbname = request.form
    requirements_input = ""
    first = True
    for key in cbname:
        if key != 'userId' and key != 'submit' and key != 'requirements_output' and key != 'weights':
            if first:
                first = False;
            else:
                requirements_input += ","
            requirements_input += key
    weights = request.form.get("weights")
    project = utils.get_project_from_db(projectId)
    print ("entry: " + str(projectId) + ", " + userId + ", " + str(requirements_input) + ", " + str(requirements_output))
    ent = utils.update_entry(projectId, userId, requirements_input,requirements_output, weights)
    user = utils.get_user_from_db(userId)
    if user.type == 'Admin':
        return show_entrys_given_project(projectId)
    elif user.type == 'User':
        return show_entrys_given_user(userId)
    else:
        return "Invalid URL", 404

@app.route('/api/v1/show_users/<projectId>')
@requires_auth
def show_users(projectId):
    users = utils.get_users_from_db(projectId)
    return render_template(
        'users.html',
        current_user=request.authorization.username,
        users= users,
        projectId = projectId)

@app.route('/api/v1/show_user/<projectId>/<identity>')
@requires_auth
def show_user(projectId, identity):
    user = utils.get_user_from_db(identity)
    projects = utils.get_projects_from_db(None)
    if user is not None and identity != "___CREATE___" :
        # edit current/existing user
        return render_template(
            'user.html',
            current_user = request.authorization.username,
            projects=projects,
            user=user)
    else:
        # edit/create user for a projectId
        if projectId and projectId !=  "__CREATE__":
            if projectId == "None":
                projectId = None
            project = utils.get_project_from_db(projectId)
            return render_template(
                'user.html',
                current_user=request.authorization.username,
                defaultPassword=project.defaultPassword,
                projectId=projectId)
        else:
            # create new user
            return render_template(
                'user.html',
                 current_user=request.authorization.username,
                 projects=projects)

@app.route('/api/v1/submitted_user', methods=['POST', 'GET'])
@requires_auth
def submitted_user():
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    userId = request.form.get('identity')
    if userId == "superuser":
        return render_template(
            "entry_error.html",
            h1Message="User ID Error, Go back and re-enter",
            title="User Add Error",
            mesage=userId + " is a system user, Please go back and use another identity and submit")
    email = request.form.get('email')
    type = request.form.get('type')
    password = request.form.get('password')
    projectIds = request.form.getlist('projectIds')
    projectId = request.form.get("projectId")
    if projectId:
        projectIds.append(projectId)
    print "user: " + str(userId) + ", " + str(email) + ", " + str(type) + ", " + str(password) + ", "  + str(projectIds)
    user = utils.update_user(userId, email, type, password, projectIds)
    current_user = utils.get_user_from_db(request.authorization.username)
    if current_user.type == "Superuser":
        return show_users(None)
    else:
        return show_project(projectId)


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

@app.route('/api/v1/show_settings', methods=['GET'])
@requires_auth
def show_settings():
    current_user = request.authorization.username
    print "show_settings for " + current_user
    return "OK", 200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.context_processor
def utility_functions():

    def get_project_status(projectId):
        return utils.get_project_status(projectId)

    def print_in_console(message):
        print str(message)

    return dict(get_project_status=get_project_status, mdebug=print_in_console)

# [END app]