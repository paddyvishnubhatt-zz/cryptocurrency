# [START imports]
from google.appengine.ext import ndb
from flask_login import UserMixin
#[END imports]

DEFAULT_PROJECT_NAME = 'cryptocurrency_project_db'

def project_db_key(project_db_name=DEFAULT_PROJECT_NAME):
    return ndb.Key('Project', project_db_name)

# [START User]
class User(ndb.Model, UserMixin):
    identity = ndb.StringProperty(indexed=True,required=True)
    email = ndb.StringProperty(indexed=True,required=True)
    type = ndb.StringProperty()
    password = ndb.StringProperty()
    token = ndb.StringProperty()

    def get_id(self):
        return self.identity
