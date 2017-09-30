
import json
import time
import datetime
from google.appengine.api import mail
from google.appengine.api import app_identity
import urllib2

from models.models import User
from models.models import DEFAULT_PROJECT_NAME
from models.models import project_db_key

firebase_server_key = "key=AIzaSyDxwE1m7WjI6400WD9GadNJqoZfJvBmjGs"
fcm_server = "https://fcm.googleapis.com/fcm/send"
fcm_headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization' : firebase_server_key}
sender_address = "DAR Admin <jaisairam0170@gmail.com>   "
total_max_limit = 1000
gae_environments = {'cryptocurrency-1003' : 'yellow'}
super_user_name = "Superuser"

CREATE_MODE = "__CREATE__"
ENTRY_SAVED_TITLE = "DAR Entry Saved"
ENTRY_SAVED_MESSAGE = "Hello {toUser}, {aboutUser} has just saved DAR entry"
DAR_TITLE = 'This is my {string} formatted with {args} arguments'
PROJECT_REMINDER_TITLE = "DAR Project Reminder ({env}) : Your DAR needs to completed"
PROJECT_REMINDER_MESSAGE = "As an admin your DAR {projectId} in {env} environment, \
                                it needs to be attended to, please remind users using Manage button"

def get_project_db_name(rname=DEFAULT_PROJECT_NAME):
    return rname

def get_users_from_db(projectId=None):
    if projectId and projectId != "":
        project = get_project_from_db(projectId)
        if project is not None:
            userIds = project.userIds
            users = []
            for userId in userIds:
                user = get_user_from_db(userId)
                users.append(user)
            return users
    else:
        users_q = User.query(User.type != super_user_name)
        users = users_q.fetch(total_max_limit)
        return users

    return None

def get_user_from_db(userId):
    if "@" in userId:
        users_q = User.query(User.email == userId)
    else:
        users_q = User.query(User.identity == userId)
    if users_q.count() < 1:
        return None
    else:
        return users_q.fetch(1)[-1]

def update_users_project(projectId, userIds):
    project = get_project_from_db(projectId)
    project.userIds = userIds
    project.put()
    return project

def update_user(userId, email, type, password, projectIds):
    user = get_user_from_db(userId)
    if user is None:
        project_name = get_project_db_name()
        user = User(parent=project_db_key(project_name))
        user.identity = userId
        user.projectIds = []
    user.email = email
    user.type = type
    user.password = password
    if projectIds:
        for projId in projectIds:
            if projId and projId != CREATE_MODE and projId not in user.projectIds:
                    user.projectIds.append(projId)
                    project = get_project_from_db(projId)
                    if project:
                        project.userIds.append(userId)
                        project.put()

    user.put()
    time.sleep(1)

    #repeat to create empty entrys by default
    if projectIds:
        for projId in projectIds:
            project = get_project_from_db(projId)
            if project:
                entry = get_entry_from_db(projId, userId)
                if entry is None:
                    update_entry(projId, userId, None, None, None, None)

    return user

def get_admin_user(projectId):
    users = get_users_from_db(projectId)
    for user in users:
        if user.type != "User":
            return user
    return None

def run_manage():
    gae_app_id = app_identity.get_application_id()
    gae_env = None
    if gae_app_id in gae_environments:
        gae_env = gae_environments[gae_app_id]
        print "Running in " + gae_env + " : " + gae_app_id
    else:
        print 'Running in ' + gae_app_id
    if gae_app_id is None and gae_env is None:
        gae_env = "purple"
    project_query = Project.query()
    projects = project_query.fetch(total_max_limit)
    if projects:
        print "Managing " + str(len(projects))
    count = 0
    for project in projects:
        print project.projectId
        count += 1
        if count > 5    :
            time.sleep(2)
        status, percentage = get_project_status(project.projectId)
        print "\t" + str(status) + ", " + str(percentage)
        if status != "OK" or percentage < 100:
            user = get_admin_user(project.projectId)
            print "\tAdmin to " + project.projectId + " is " + user.identity
            if user:
                title = PROJECT_REMINDER_TITLE.format(env=gae_env)
                message = PROJECT_REMINDER_MESSAGE.format(projectId=project.projectId, env=gae_env)
                send_message(user, title, message)
                time.sleep(2)

def send_message(user, title, message):
    print "Sending email to " + user.email
    mail.send_mail(sender=sender_address,
                   to=user.email,
                   subject=title,
                   body=message)
    if hasattr(user, 'token') and user.token:
        send_notification(user.token, title, message)

def send_notification(toaddr, title, content):
    print 'send_notification ' + toaddr + ", " + title + ", " + content
    headers = fcm_headers
    url = fcm_server
    data = {'priority': 'high', 'to': toaddr, \
            'notification' : {'badge': '1', 'sound' : 'default', 'title' : title, 'body' : content}}
    try:
        opener = urllib2.build_opener()
        req = urllib2.Request(url, data=json.dumps(data), headers=headers)
        resp = opener.open(req)
        print "OK - Notification sent"
    except urllib2.HTTPError as e:
        error_message = e.read()
        print error_message

def update_token(userId, token):
    print "In update_token: " + userId + ", " + token
    user = get_user_from_db(userId)
    if user.token != token:
        user.token = token
        user.put()

def get_user_type_from_db(identity):
    user = get_user_from_db(identity)
    return user.type
