
from register import Entry
from register import User
from register import Register
from register import DEFAULT_REGISTER_NAME
from register import register_key

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
    register_name = get_register_name()
    register_query = Register.query(
        ancestor=register_key(register_name))

    for register in register_query:
        if register.registerId == registerId:
            return register

    return None

def get_entry_from_db_given_user(userId):
    print "userId " + userId
    register_name = get_register_name()
    entrys_query = Entry.query(
        ancestor=register_key(register_name)).order(-Entry.date)

    entrys = entrys_query.fetch(100)
    for entry in entrys:
        if userId == entry.user.identity:
            return entry

    return None

def get_entry_from_db_given_date(date):
    register_name = get_register_name()
    entrys_query = Entry.query(
        ancestor=register_key(register_name)).order(-Entry.date)

    entrys = entrys_query.fetch(100)
    for entry in entrys:
        datestr = entry.date.strftime("%Y-%m-%d% %H:%M:%S.%f")
        if date == datestr:
            return entry

    return None

def get_entrys_from_db(registerId):
    register_name = get_register_name()
    entrys_query = Entry.query(
        ancestor=register_key(register_name)).order(-Entry.date)

    entrys = entrys_query.fetch(100)
    returnEntrys = []
    for entry in entrys:
        if entry.register.registerId == registerId:
            returnEntrys.append(entry)

    return returnEntrys

def get_users_from_db(registerId):
    register = get_register_from_db(registerId)
    returnUsers = register.users
    return returnUsers

def get_user_from_db(userId):
    register_name = get_register_name()
    users_query = User.query(
        ancestor=register_key(register_name))

    users = users_query.fetch(100)
    for user in users:
        if user.identity == userId:
            return user

    return None

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
        register_name = get_register_name()
        register = Register(parent=register_key(register_name))
        register.registerId = registerId
        register.requirements = requirement_items
        userstrings = ["user1", "user2", "user3", "user4"]
        users = []
        for userName in userstrings:
            user = User(parent=register_key(register_name))
            user.identity = userName
            user.email = userName + "@sellerforce.com"
            user.put()
            users.append(user)
        register.users = users
        register.put()
        return register

def store_entry(registerId, userId, cbname):
    register_name =  DEFAULT_REGISTER_NAME
    entry = Entry(parent=register_key(register_name))
    entry.user = get_user_from_db(userId)
    entry.register = get_register_from_db(registerId)
    requirements = []
    for key in cbname:
        requirements.append(key)
    entry.requirements = requirements
    entry.put()