
from register import Entry
from register import User
from register import Register
from register import DEFAULT_REGISTER_NAME
from register import register_key
from functools import wraps
import time

from flask import request, Response, url_for, redirect
from google.appengine.ext import ndb

def get_register_name(rname=DEFAULT_REGISTER_NAME):
    return rname

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_registers_from_db():
    register_name = get_register_name()
    register_query = Register.query(
        ancestor=register_key(register_name))

    return register_query.fetch(100)

#Gets requirements from db - this needs to implement requirements-lifecycle - right now it is a singleton
def get_register_from_db(registerId):
    if registerId is None:
        registerId = "SingletonRegister"
    register_query = Register.query(Register.registerId == registerId)
    if register_query.count() < 1:
        return None
    else:
        return register_query.fetch(1)[-1]

def get_entry_from_db_given_user(registerId, userId):
    entrys_query = Entry.query(Entry.user.identity == userId, Entry.register.registerId == registerId)
    if entrys_query.count() < 1:
        return None
    else:
        return entrys_query.fetch(1)[-1]

def get_entrys_from_db(registerId):
    entrys_query = Entry.query(Entry.register.registerId == registerId)
    entrys = entrys_query.fetch(100)
    returnEntrys = []
    for entry in entrys:
        if entry.register.registerId == registerId:
            returnEntrys.append(entry)

    return returnEntrys

def get_users_from_db(registerId=None):
    if registerId and registerId != "":
        print registerId
        register = get_register_from_db(registerId)
        returnUsers = register.users
        return returnUsers
    else:
        users_q = User.query(User.type != "Superuser")
        users = users_q.fetch(100)
        return users

def get_user_from_db(userId):
    users_q = User.query(User.identity == userId)
    if users_q.count() < 1:
        return None
    else:
        return users_q.fetch(1)[-1]

def update_users_register(registerId, userIds):
    register = get_register_from_db(registerId)
    users = []
    for userName in userIds:
        user = get_user_from_db(userName)
        users.append(user)
    register.users = users
    register.put()
    return register

def update_user(userId, email, type, password, registerId):
    user = get_user_from_db(userId)
    if user is None:
        register_name = get_register_name()
        user = User(parent=register_key(register_name))
        user.identity = userId
    user.email = email
    user.type = type
    user.password = password
    user.defaultRegisterId = registerId
    user.put()
    if registerId and registerId != "__CREATE__":
        print registerId
        register = get_register_from_db(registerId)
        users = register.users
        users.append(user)
        register.put()
    time.sleep(1)
    return user

def update_register(registerId, department, group, description, userIds, requirements):
    register_name = get_register_name()
    register = get_register_from_db(registerId)
    if register is None:
        register = Register(parent=register_key(register_name))
        register.registerId = registerId

    register.requirements = requirements.split(",")
    register.department = department
    register.description = description
    register.group = group
    users = []
    for userName in userIds:
        user = get_user_from_db(userName)
        users.append(user)
    register.users = users
    register.put()
    return register

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
        requirement_items.append("popularity")
        register_name = get_register_name()
        register = Register(parent=register_key(register_name))
        register.registerId = registerId
        register.requirements = requirement_items
        register.department = "Department-Q"
        register.group = "lawn-mowers"
        register.description = "This requirement is for lawn mowers but could be applied to dish washers also"
        register.defaultPassword = "nowisthetime"
        userstrings = ["user1", "user2", "user3", "user4"]
        users = []
        for userName in userstrings:
            user = User(parent=register_key(register_name))
            user.identity = userName
            user.email = userName + "@sellerforce.com"
            user.password = register.defaultPassword
            user.defaultRegisterId = registerId
            if user.identity == "user2":
                user.type = "Admin"
            else:
                user.type = "User"
            user.put()
            users.append(user)
        register.users = users
        register.put()
        return register

def create_entry(registerId, userId, requirements_input):
    register_name =  DEFAULT_REGISTER_NAME
    entry = Entry(parent=register_key(register_name))
    entry.user = get_user_from_db(userId)
    entry.register = get_register_from_db(registerId)
    requirements = []
    for key in requirements_input:
        requirements.append(key)
    entry.requirements = requirements
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