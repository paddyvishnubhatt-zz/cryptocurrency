# [START imports]
from google.appengine.ext import ndb
from flask_login import UserMixin
#[END imports]

DEFAULT_PROJECT_NAME = 'default_project_db'

def project_db_key(project_db_name=DEFAULT_PROJECT_NAME):
    return ndb.Key('Project', project_db_name)

# [START User]
class User(ndb.Model, UserMixin):
    identity = ndb.StringProperty(indexed=True,required=True)
    email = ndb.StringProperty(indexed=True,required=True)
    type = ndb.StringProperty()
    isFirstLogin = ndb.BooleanProperty(default=True)
    password = ndb.StringProperty()
    projectIds = ndb.StringProperty(repeated=True)
    token = ndb.StringProperty()

    def get_id(self):
        return self.identity

# [START Requirement]
class EvaluationCriteria(ndb.Model):
    evaluation_criterionId = ndb.StringProperty(indexed=True, required=True)
    projectId = ndb.StringProperty(required=True)
    objectiveId = ndb.StringProperty(required=True)
    evaluation_criterion = ndb.StringProperty()
    calculations = ndb.JsonProperty()

# [START Objective]
class Objective(ndb.Model):
    objectiveId = ndb.StringProperty(indexed=True, required=True)
    projectId = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    weight = ndb.IntegerProperty()
    evaluation_criteriaIds = ndb.StringProperty(repeated=True)

# [START Project]
class Project(ndb.Model):
    projectId = ndb.StringProperty(indexed=True, required=True)
    objectiveIds = ndb.StringProperty(repeated=True)
    due_date = ndb.DateTimeProperty(required=True)
    userIds = ndb.StringProperty(repeated=True)
    vendorIds = ndb.StringProperty(repeated=True)
    defaultPassword = ndb.StringProperty()
    department = ndb.StringProperty()
    group = ndb.StringProperty()
    description = ndb.StringProperty()

# [START Entry]
class Entry(ndb.Model):
    project = ndb.StructuredProperty(Project, indexed=True, required=True)
    user = ndb.StructuredProperty(User, indexed=True, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    weights = ndb.StringProperty(repeated=True)
    evaluation_criteria = ndb.StringProperty(repeated=True)
    evaluation_criteria_output = ndb.StringProperty(repeated=True)
    vendor_output = ndb.JsonProperty()

# [START Vendor]
class Vendor(ndb.Model):
    identity = ndb.StringProperty(indexed=True,required=True)
    email = ndb.StringProperty(indexed=True,required=True)
    projectIds = ndb.StringProperty(repeated=True)
