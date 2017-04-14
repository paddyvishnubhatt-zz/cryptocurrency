import logging
import utils
from flask import Flask, session, render_template, request, url_for, redirect
import datetime
from utils import requires_auth
import json
import urllib
from markupsafe import Markup
import time
from flask import send_from_directory
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def root():
    return render_template('root.html')


@app.route('/request_for_admin')
def request_for_admin():
    return render_template('admin_request.html')

@app.route('/check_auth')
@requires_auth
def check_auth():
    return "OK", 200

@app.route('/api/v1/about_page')
@requires_auth
def about_page():
    return render_template(
        'about.html',
        current_user=request.authorization.username)

@app.route('/api/v1/admin_page')
@requires_auth
def admin_page():
    return render_template(
        'admin.html',
        current_user=request.authorization.username)

@app.route('/api/v1/landing_page')
@requires_auth
def landing_page():
    user = utils.get_user_from_db(request.authorization.username)
    if user.type == "Admin":
        return show_projects()
    elif user.type == "Superuser":
        return admin_page()
    else:
        return show_entrys_given_user(user.identity)

@app.route('/api/v1/show_projects')
@requires_auth
def show_projects():
    current_user = request.authorization.username
    if utils.checkIfAdminUser() == False:
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
    if utils.checkIfAdminUser() == False:
        return "Unauthorized", 404
    vendor_objs = utils.get_vendors_from_db(None)
    users = utils.get_users_from_db(None)
    if projectId is not None and projectId != "___CREATE___" :
        project = utils.get_project_from_db(projectId)
        userlist = project.userIds
        vendorlist = project.vendorIds
        bos_db, cs = utils.get_business_objectives_from_db(projectId, False)
        return render_template(
            'project.html',
            current_user=request.authorization.username,
            project=project,
            vendorlist = vendorlist,
            vendor_objects=vendor_objs,
            userlist = userlist,
            bos_db = bos_db,
            users=users)
    else:
        return render_template(
            'project.html',
            current_user=request.authorization.username,
            vendor_objects=vendor_objs,
            users=users)

@app.route('/api/v1/submitted_project', methods=['POST', 'GET'])
@requires_auth
def submitted_project():
    if utils.checkIfAdminUser() == False:
        return "Unauthorized", 404
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    projectId = request.form.get('projectId')
    # todo
    # tprj = utils.get_project_from_db(projectId)
    #if tprj:
    #    return render_template(
    #        'entry_error.html',
    #        h1Message = "   Error: Project ID Already Exists",
    #        message = "  Project " + projectId + " already exists.Go Back and retry w/ another ID"
    #    )
    userIds = set(request.form.getlist('userIds[]'))
    vendorIds = set(request.form.getlist('vendorIds[]'))
    bos = request.form.getlist("bos[]")
    due_date = request.form.get('due_date')
    department = request.form.get('department')
    group = request.form.get('group')
    description = request.form.get('description')
    defaultPassword = request.form.get('password')
    userId = request.authorization.username
    if userId not in userIds:
        userIds.add(userId)
    utils.update_project(projectId, department, group, description, defaultPassword, userIds, vendorIds, due_date, bos)
    time.sleep(1)
    return redirect(url_for('landing_page'))

@app.route('/api/v1/show_summary/<projectId>')
@requires_auth
def show_summary(projectId):
    if utils.checkIfAdminUser() == False:
        return "Unauthorized", 404
    userId = request.authorization.username
    start = time.clock()
    bos_db, criteria_to_users_map = utils.get_business_objectives_from_db(projectId, True)
    print str(time.clock() - start)
    project = utils.get_project_from_db(projectId)
    return render_template(
        'summary.html',
        current_user=request.authorization.username,
        project = project,
        bos_db = bos_db,
        criteria_to_users_map = criteria_to_users_map,
        userId = userId)

@app.route('/api/v1/show_entry/<projectId>/<userId>')
@requires_auth
def show_entry(projectId, userId):
    project = utils.get_project_from_db(projectId)
    bos_db, cs = utils.get_business_objectives_from_db(projectId, True)
    entry = utils.get_entry_from_db(projectId, userId)
    return render_template(
        'entry.html',
        current_user=request.authorization.username,
        userId = userId,
        project=project,
        bos_db = bos_db,
        entry=entry)

@app.route('/api/v1/show_entrys_given_project/<projectId>')
@requires_auth
def show_entrys_given_project(projectId):
    isAdminUser = utils.checkIfAdminUser()
    if isAdminUser == False:
        return "Unauthorized", 404
    users = utils.get_users_from_db(projectId)
    entrys = []
    for user in users:
        entry = utils.get_entry_from_db(projectId, user.identity)
        if entry is None:
            entry = utils.update_entry(projectId, user.identity, None, None, None,None)
        entrys.append(entry)

    userId = request.authorization.username
    return render_template(
        'entrys.html',
        current_date=datetime.datetime.now(),
        current_user=request.authorization.username,
        projectId = projectId,
        userId = userId,
        isAdminUser = isAdminUser,
        entrys= entrys)

@app.route('/api/v1/show_entrys_given_user/<userId>')
@requires_auth
def show_entrys_given_user(userId):
    entrys = []
    projects = utils.get_projects_from_db(userId)
    for project in projects:
        entry = utils.get_entry_from_db(project.projectId, userId)
        if entry is None:
            entry = utils.update_entry(project.projectId, userId, None, None, None, None)
        entrys.append(entry)
    return render_template(
        'entrys.html',
        current_date=datetime.datetime.now(),
        current_user=request.authorization.username,
        userId = userId,
        entrys= entrys)

@app.route('/api/v1/submitted_entry/<projectId>', methods=['POST', 'GET'])
@requires_auth
def submitted_entry(projectId):
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    userId = request.authorization.username
    evaluation_criteria_output = request.form.get("evaluation_criteria_output")
    vendor_output = request.form.get("vendor_output")
    weights = request.form.get("weights")
    cbname = request.form
    evaluation_criteria_input = ""
    first = True
    for key in cbname:
        if key != 'userId' and key != 'submit' and key != 'evaluation_criteria_output' and key != 'weights':
            if first:
                first = False
            else:
                evaluation_criteria_input += ","
            evaluation_criteria_input += key
    print ("entry: " + str(projectId) + ", " + userId +  ", " + str(evaluation_criteria_output) + ", " + str(weights))
    ent = utils.update_entry(projectId, userId, evaluation_criteria_input,evaluation_criteria_output, vendor_output, weights)
    user = utils.get_user_from_db(userId)
    if user.type == 'Admin':
        return redirect(url_for('show_entrys_given_project', projectId=projectId))
    elif user.type == 'User':
        utils.send_entry_completion(projectId, userId)
        return redirect(url_for('show_entrys_given_user', userId=userId))
    else:
        return "Invalid URL", 404

@app.route('/api/v1/show_users')
@requires_auth
def show_users():
    users = utils.get_users_from_db(None)
    return render_template(
        'users.html',
        current_user=request.authorization.username,
        users= users)

@app.route('/api/v1/submitted_admin_user', methods=['POST'])
def submitted_admin_user():
    username = request.form.get('username')
    user = utils.get_user_from_db(username)
    if user:
        return render_template(
            "entry_error.html",
            h1Message="User ID Error, Go back and re-enter",
            title="User Add Error",
            message=username + " already is an existing user, Please go back and use another identity and submit")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = utils.update_user(username, email, "Admin", password, None)
        try:
            utils.send_message(user, "DAR Admin User Created", "Admin user for " + username + \
                               " created. Please go ahead and create DAR project and add/invite users to the project")
        except RuntimeError as e:
            print e
        return render_template('root.html')

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
            message=userId + " is a system user, Please go back and use another identity and submit")
    email = request.form.get('email')
    type = request.form.get('type')
    password = request.form.get('password')
    projectIds = request.form.getlist('projectIds[]')
    projectId = request.form.get("projectId")
    newProject = False
    if projectId and projectId not in projectIds:
        projectIds.append(projectId)
        newProject = True
    print "user: " + str(userId) + ", " + str(email) + ", " + str(type) + ", " + str(password) + ", "  + str(projectIds)
    user = utils.update_user(userId, email, type, password, projectIds)
    if newProject:
        utils.send_message(user, "Welcome to DAR " + projectId,
                           "Hello " + user.identity + "\nYou have been chosen as a subject matter expert to help w/ DAR " + \
                           projectId + ", please login and complete your entry, Thank you.")
    current_user = utils.get_user_from_db(request.authorization.username)
    if current_user.type == "Superuser":
        return redirect(url_for('show_users'))
    else:
        return redirect(url_for('show_project', projectId=projectId))

@app.route('/api/v1/show_vendors')
@requires_auth
def show_vendors():
    vendors = utils.get_vendors_from_db(None)
    return render_template(
        'vendors.html',
        current_user=request.authorization.username,
        vendors= vendors)

@app.route('/api/v1/show_vendor/<projectId>/<identity>')
@requires_auth
def show_vendor(projectId, identity):
    vendor = utils.get_vendor_from_db(identity)
    projects = utils.get_projects_from_db(None)
    if vendor is not None and identity != "___CREATE___" :
        # edit current/existing vendor
        return render_template(
            'vendor.html',
            current_user = request.authorization.username,
            projects=projects,
            vendor=vendor)
    else:
        # edit/create vendor for a projectId
        if projectId and projectId !=  "__CREATE__":
            if projectId == "None":
                projectId = None
            project = utils.get_project_from_db(projectId)
            return render_template(
                'vendor.html',
                current_user=request.authorization.username,
                defaultPassword=project.defaultPassword,
                projectId=projectId)
        else:
            # create new vendor
            return render_template(
                'vendor.html',
                 current_vendor=request.authorization.username,
                 projects=projects)

@app.route('/api/v1/submitted_vendor', methods=['POST', 'GET'])
@requires_auth
def submitted_vendor():
    if request.method == 'GET':
        return redirect(url_for('landing_page'))
    vendorId = request.form.get('identity')
    email = request.form.get('email')
    projectIds = request.form.getlist('projectIds[]')
    projectId = request.form.get("projectId")
    if projectId:
        projectIds.append(projectId)
    print "vendor: " + str(vendorId) + ", " + str(email) + ", " + ", "  + str(projectIds)
    vendor = utils.update_vendor(vendorId, email, projectIds)
    return show_vendors()

@app.route('/api/v1/send_email', methods=['POST'])
def send_email():
    content =  request.form.get('content')
    tolist = request.form.getlist('tolist[]')
    title = "DAR Entry Reminder: Your DAR entry needs to completed"
    utils.send_reminders(tolist, title, content)
    return "OK", 200

@app.route('/api/v1/manage', methods=['GET', 'POST'])
def manage():
    utils.run_manage()
    return "OK", 200

@app.route('/api/v1/update_token', methods=['POST'])
def update_token():
    if request.authorization is None or 'username' not in session:
        print request.authorization
        return "OK", 200
    if request.authorization:
        username = request.authorization.username
    if 'username' in session:
        print session
        username = session['username']
    token = request.form.get('token')
    utils.update_token(request.authorization.username, token)
    return "OK", 200

@app.route('/api/v1/delete_project/<projectId>', methods=['DELETE'])
@requires_auth
def delete_project(projectId):
    utils.delete_project_from_db(projectId)
    return "OK", 200

@app.route('/api/v1/delete_user/<userId>', methods=['DELETE'])
@requires_auth
def delete_user(userId):
    utils.delete_user_from_db(userId)
    return "OK", 200

@app.route('/api/v1/delete_users', methods=['DELETE'])
@requires_auth
def delete_users():
    utils.delete_users_from_db()
    return "OK", 200

@app.route('/api/v1/delete_vendor/<vendorId>', methods=['DELETE'])
@requires_auth
def delete_vendor(vendorId):
    utils.delete_vendor_from_db(vendorId)
    return "OK", 200

@app.route('/api/v1/delete_vendors', methods=['DELETE'])
@requires_auth
def delete_vendors():
    utils.delete_vendors_from_db()
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

    def get_entry_status(projectId, userId):
        return utils.get_entry_status(projectId, userId)

    def get_project_status(projectId):
        return utils.get_project_status(projectId)

    def print_in_console(message):
        print str(message)

    def str_to_obj(str):
        return eval(str)

    def get_current_date():
        import datetime
        return datetime.date.today().strftime("%Y-%m-%d")

    @app.template_filter('urlencode')
    def urlencode_filter(s):
        if type(s) == 'Markup':
            s = s.unescape()
        s = s.encode('utf8')
        s = urllib.quote(s)
        return Markup(s)

    app.jinja_env.globals['urlencode'] = urlencode_filter
    return dict(get_entry_status=get_entry_status, urlencode=urlencode_filter, get_project_status=get_project_status, mdebug=print_in_console, str_to_obj=str_to_obj, get_current_date=get_current_date)

# [END app]