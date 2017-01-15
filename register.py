# [START imports]
import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_REGISTER_NAME = 'default_register'

def register_key(register_name=DEFAULT_REGISTER_NAME):
    return ndb.Key('Register', register_name)

# [START Author]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

# [START Register]
class Register(ndb.Model):
    registerId = ndb.StringProperty(indexed=True)
    users = ndb.StringProperty(repeated=True)
    requirements = ndb.StringProperty(repeated=True)

# [START Entry]
class Entry(ndb.Model):
    """Sub model for representing an author."""
    register = ndb.StructuredProperty(Register)
    author = ndb.StructuredProperty(Author)
    date = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    requirements = ndb.StringProperty(repeated=True)