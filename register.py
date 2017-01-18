# [START imports]
from google.appengine.ext import ndb
#[END imports]

DEFAULT_REGISTER_NAME = 'default_register'

def register_key(register_name=DEFAULT_REGISTER_NAME):
    return ndb.Key('Register', register_name)

# [START User]
class User(ndb.Model):
    identity = ndb.StringProperty(indexed=True,required=True)
    email = ndb.StringProperty(indexed=True,required=True)

# [START Register]
class Register(ndb.Model):
    registerId = ndb.StringProperty(indexed=True,required=True)
    users = ndb.StructuredProperty(User, repeated=True)
    requirements = ndb.StringProperty(repeated=True)

# [START Entry]
class Entry(ndb.Model):
    """Sub model for representing an author."""
    register = ndb.StructuredProperty(Register, indexed=True, required=True)
    user = ndb.StructuredProperty(User, indexed=True, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    requirements = ndb.StringProperty(repeated=True)