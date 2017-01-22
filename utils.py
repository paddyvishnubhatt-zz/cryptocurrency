
from models import Entry
from models import User
from models import Project
from models import DEFAULT_PROJECT_NAME
from models import project_db_key
from functools import wraps
import time
from flask import request, Response, url_for, redirect

def get_project_db_name(rname=DEFAULT_PROJECT_NAME):
    return rname

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_projects_from_db():
    project_name = get_project_db_name()
    project_query = Project.query(
        ancestor=project_db_key(project_name))

    return project_query.fetch(100)

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_project_from_db(projectId):
    project_query = Project.query(Project.projectId == projectId)
    if project_query.count() < 1:
        return None
    else:
        return project_query.fetch(1)[-1]

def get_entry_from_db(projectId, userId):
    entrys_query = Entry.query(Entry.user.identity == userId, Entry.project.projectId == projectId)
    if entrys_query.count() < 1:
        return None
    else:
        return entrys_query.fetch(1)[-1]

def get_entrys_from_db(projectId):
    entrys_query = Entry.query(Entry.project.projectId == projectId)
    entrys = entrys_query.fetch(100)
    returnEntrys = []
    for entry in entrys:
        if entry.project.projectId == projectId:
            returnEntrys.append(entry)

    return returnEntrys

def get_users_from_db(projectId=None):
    if projectId and projectId != "":
        project = get_project_from_db(projectId)
        if project is not None:
            return project.users
    else:
        users_q = User.query(User.type != "Superuser")
        users = users_q.fetch(1000)
        return users

    return None

def get_user_from_db(userId):
    users_q = User.query(User.identity == userId)
    if users_q.count() < 1:
        return None
    else:
        return users_q.fetch(1)[-1]

def update_users_project(projectId, userIds):
    project = get_project_from_db(projectId)
    users = []
    for userName in userIds:
        user = get_user_from_db(userName)
        users.append(user)
    project.users = users
    project.put()
    return project

def update_user(userId, email, type, password, projectId):
    user = get_user_from_db(userId)
    if user is None:
        project_name = get_project_db_name()
        user = User(parent=project_db_key(project_name))
        user.identity = userId
    user.email = email
    user.type = type
    user.password = password
    user.defaultProjectId = projectId
    user.put()
    if projectId and projectId != "__CREATE__":
        project = get_project_from_db(projectId)
        if project:
            users = project.users
            users.append(user)
            project.put()
    time.sleep(1)
    return user

def update_project(projectId, department, group, description, userIds, requirements):
    project_name = get_project_db_name()
    project = get_project_from_db(projectId)
    if project is None:
        project = Project(parent=project_db_key(project_name))
        project.projectId = projectId
    project.requirements = requirements.split(",")
    project.department = department
    project.description = description
    project.group = group
    users = []
    for userName in userIds:
        user = get_user_from_db(userName)
        users.append(user)
    project.users = users
    project.put()
    return project

def delete_project_from_db(projectId):
    project = get_project_from_db(projectId)
    entrys = get_entrys_from_db(projectId)
    for entry in entrys:
        key = entry.key
        print "entry: " + str(key)
        if key:
            key.delete()
    key = project.key
    if key:
        key.delete()

def delete_users_from_db():
    users = get_users_from_db(None)
    if users:
        for user in users:
            key = user.key
            print "user: " + str(key)
            if key:
                key.delete()

def create_entry(projectId, userId, requirements_input):
    project_name =  DEFAULT_PROJECT_NAME
    entry = Entry(parent=project_db_key(project_name))
    entry.user = get_user_from_db(userId)
    entry.project = get_project_from_db(projectId)
    entry.requirements = requirements_input
    entry.put()
    return entry

def check_auth(identity, password):
    """This function is called to check if a username /
        password combination is valid.
        """
    user = get_user_from_db(identity)
    if user:
        return True
    else:
        if identity == 'admin' and password == 'password':
            update_user('admin', 'admin@lafoot.com', 'Superuser', 'password', None)
            return True
        else:
            return False

def get_user_type_from_db(identity):
    user = get_user_from_db(identity)
    return user.type

def is_user_first_login(identity):
    user = get_user_from_db(identity)
    return user.isFirstLogin

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        else:
            return f(*args, **kwargs)

    return decorated