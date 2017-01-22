# [START imports]
from google.appengine.ext import ndb
#[END imports]

DEFAULT_PROJECT_NAME = 'default_project_db'

def project_db_key(project_db_name=DEFAULT_PROJECT_NAME):
    return ndb.Key('Project', project_db_name)

# [START User]
class User(ndb.Model):
    identity = ndb.StringProperty(indexed=True,required=True)
    email = ndb.StringProperty(indexed=True,required=True)
    defaultProjectId = ndb.StringProperty()
    type = ndb.StringProperty()
    isFirstLogin = ndb.BooleanProperty(default=True)
    password = ndb.StringProperty()

# [START Project]
class Project(ndb.Model):
    projectId = ndb.StringProperty(indexed=True, required=True)
    users = ndb.StructuredProperty(User, repeated=True)
    requirements = ndb.StringProperty(repeated=True)
    defaultPassword = ndb.StringProperty()
    department = ndb.StringProperty()
    group = ndb.StringProperty()
    description = ndb.StringProperty()

# [START Entry]
class Entry(ndb.Model):
    """Sub model for representing an author."""
    project = ndb.StructuredProperty(Project, indexed=True, required=True)
    user = ndb.StructuredProperty(User, indexed=True, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    requirements = ndb.StringProperty(repeated=True)