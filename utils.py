
from models import Entry
from models import User
from models import Project
from models import Vendor
from models import Objective
from models import EvaluationCriteria
from models import DEFAULT_PROJECT_NAME
from models import project_db_key
from functools import wraps
import json
import time
import datetime
from flask import request, Response, url_for, redirect

def get_project_db_name(rname=DEFAULT_PROJECT_NAME):
    return rname

#Gets evaluation_criteria from db - this needs to implement evaluation_criteria-lifecycle - right now it is a singleton
def get_projects_from_db(userId):
    if userId:
        project_query = Project.query(Project.userIds.IN([userId]))
    else:
        project_query = Project.query()
    return project_query.fetch(100)

#Gets evaluation_criteria from db - this needs to implement evaluation_criteria-lifecycle - right now it is a singleton
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

def get_entrys_from_given_project_db(projectId):
    entrys_query = Entry.query(Entry.project.projectId == projectId)
    return entrys_query.fetch(100)

def get_entrys_from_given_user_db(userId):
    user = get_user_from_db(userId)
    entrys_query = Entry.query(Entry.user == user)
    return entrys_query.fetch(100)

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
        users_q = User.query(User.type != "Superuser")
        users = users_q.fetch(1000)
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
            if projId and projId != "__CREATE__"and projId not in user.projectIds:
                    user.projectIds.append(projId)
                    project = get_project_from_db(projId)
                    if project:
                        project.userIds.append(userId)
                        project.put()
    user.put()
    time.sleep(1)
    return user

def getArrayOfDict(bos):
    # this is not good
    bot = bos[0]
    # this is even worse
    bot = '[' + bot + ']'
    bol = json.loads(bot)
    return bol

def update_project(projectId, department, group, description, defaultPassword, userIds, vendorIds, due_date, bos):
    project_name = get_project_db_name()
    project = get_project_from_db(projectId)
    if project is None:
        project = Project(parent=project_db_key(project_name))
        project.projectId = projectId
        project.objectiveIds = []
    project.department = department
    project.description = description
    project.group = group
    project.defaultPassword = defaultPassword
    project.userIds = userIds
    project.vendorIds = vendorIds
    for ui in userIds:
        user = get_user_from_db(ui)
        if user and projectId not in user.projectIds:
            user.projectIds.append(projectId)
            user.put()
    for vi in vendorIds:
        vendor = get_user_from_db(vi)
        if vendor and projectId not in vendor.projectIds:
            vendor.projectIds.append(projectId)
            vendor.put()
    if due_date is None or due_date == "":
        project.due_date = datetime.datetime.now()
    else:
        project.due_date = datetime.datetime.strptime(due_date.split(" ")[0], "%Y-%m-%d")
    bol = getArrayOfDict(bos)
    if len(project.objectiveIds) > 0:
        nnbos = []
        for bo in bol:
            nnbos.append(bo["objectiveId"])
        for pbo in project.objectiveIds:
            if pbo not in nnbos:
                print "deleting " + pbo
                project.objectiveIds.remove(pbo)
                delete_objective_from_db(projectId, pbo)

    for bo in bol:
        #print bo["objectiveId"] + ", " + bo["description"] + ", " + bo["weight"]
        boid = bo["objectiveId"]
        nbo = get_objective_from_db(projectId, boid)
        if nbo is None:
            nbo = Objective(parent=project_db_key(project_name))
            nbo.objectiveId = boid
            nbo.projectId = projectId
            nbo.evaluation_criteriaIds = []
        nbo.description = bo["description"]
        nbo.weight = int(bo["weight"])
        if "evaluation_criteria" in bo:
            for ec in bo["evaluation_criteria"]:
                ecid = ec["evaluation_criteriaId"]
                nec = get_evaluation_criteria_from_db(projectId, boid, ecid)
                #print "\t" + projectId + ", " + ec["evaluation_criteriaId"] + ", " + ec["evaluation_criterion"] + "\n\t" + str(nec)
                if nec is None:
                    nec = EvaluationCriteria(parent=project_db_key(project_name))
                    nec.evaluation_criterionId = ecid
                    nec.objectiveId = boid
                    nec.projectId = projectId
                nec.evaluation_criterion = ec["evaluation_criterion"]
                nec.put()
                if ecid in nbo.evaluation_criteriaIds:
                    iiidx = nbo.evaluation_criteriaIds.index(ecid)
                    pnbo.evaluation_criteriaIds[iiidx] = ecid
                else:
                    nbo.evaluation_criteriaIds.append(ecid)
        nbo.put()
        if nbo.objectiveId in project.objectiveIds:
            iidx = project.objectiveIds.index(nbo.objectiveId)
            project.objectiveIds[iidx] = nbo.objectiveId
        else:
            project.objectiveIds.append(nbo.objectiveId)

    project.put()
    return project

def get_objective_from_db(projectId, objectiveId):
    objectives_query = Objective.query(Objective.objectiveId == objectiveId,
                                       Objective.projectId == projectId)
    if objectives_query.count() < 1:
        return None
    else:
        return objectives_query.fetch(1)[-1]

def get_evaluation_criteria_from_db(projectId, objectiveId, evaluation_criterionId):
    evaluation_criteria_query = EvaluationCriteria.query(EvaluationCriteria.evaluation_criterionId == evaluation_criterionId,
                                                         EvaluationCriteria.objectiveId == objectiveId,
                                                         EvaluationCriteria.projectId == projectId)
    if evaluation_criteria_query.count() < 1:
        return None
    else:
        return evaluation_criteria_query.fetch(1)[-1]

def get_project_status(projectId):
    entrys = get_entrys_from_given_project_db(projectId)
    status = "OK"
    total = len(entrys)
    if total > 0:
        current = 0
        for entry in entrys:
            if len(entry.evaluation_criteria_output) == 0:
                project = get_project_from_db(projectId)
                cur_date = datetime.datetime.now()
                print str(project.due_date) + ", " + str(cur_date)
                if project.due_date < cur_date:
                    status = "Late"
                else:
                    if status == "OK":
                        status = "Incomplete"
            else:
                current += 1
        percentage = float (current /total) * 100
    else:
        percentage = 0
        status = "Incomplete"
    return status, percentage

def delete_objective_from_db(projectId, objectiveId):
    objective = get_objective_from_db(projectId, objectiveId)
    if objective:
        for ecid in objective.evaluation_criteriaIds:
            # print objective
            # print " *** looking for : " + objectiveId + ", " + ecid
            evaluation_criterion = get_evaluation_criteria_from_db(projectId, objectiveId, ecid)
            if evaluation_criterion:
                key = evaluation_criterion.key
                if key:
                    print '\tdeleting ' + evaluation_criterion.evaluation_criterion
                    key.delete()
        key = objective.key
        if key:
            print '\tdeleting ' + objective.objectiveId
            key.delete()


def delete_project_from_db(projectId):
    print 'deleting ' + projectId
    project = get_project_from_db(projectId)
    entrys = get_entrys_from_given_project_db(projectId)
    vendorIds = project.vendorIds
    for objectiveId in project.objectiveIds:
        delete_objective_from_db(projectId, objectiveId)
    for vid in vendorIds:
        vendor = get_vendor_from_db(vid)
        if vendor:
            key = vendor.key
            if key:
                key.delete()
    for entry in entrys:
        key = entry.key
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
            if key:
                key.delete()

def update_entry(projectId, userId, evaluation_criteria, evaluation_criteria_output, vendor_output, weights):
    entry = get_entry_from_db(projectId, userId)
    if entry is None:
        project_name =  DEFAULT_PROJECT_NAME
        entry = Entry(parent=project_db_key(project_name))
        entry.user = get_user_from_db(userId)
        entry.project = get_project_from_db(projectId)
    if evaluation_criteria:
        entry.evaluation_criteria = evaluation_criteria.split(",")
    if evaluation_criteria_output:
        entry.evaluation_criteria_output = evaluation_criteria_output.split(",")
    if weights:
        sweights = json.loads(weights)
        for weight in sweights:
            entry.weights.append(weight + ":" + str(sweights[weight]))
    if vendor_output:
        entry.vendor_output = vendor_output
    entry.put()
    return entry

def get_vendors_from_db(projectId=None):
    if projectId and projectId != "":
        project = get_project_from_db(projectId)
        if project is not None:
            vendorIds = project.vendorIds
            vendors = []
            for vendorId in vendorIds:
                vendor = get_vendor_from_db(vendorId)
                vendors.append(vendor)
            return vendors
    else:
        vendors_q = Vendor.query()
        vendors = vendors_q.fetch(1000)
        return vendors

    return None

def get_vendor_from_db(vendorId):
    vendors_q = Vendor.query(Vendor.identity == vendorId)
    if vendors_q.count() < 1:
        return None
    else:
        return vendors_q.fetch(1)[-1]

def update_vendor(vendorId, email, projectIds):
    vendor = get_vendor_from_db(vendorId)
    if vendor is None:
        project_name = get_project_db_name()
        vendor = Vendor(parent=project_db_key(project_name))
        vendor.identity = vendorId
        vendor.projectIds = []
    vendor.email = email
    if projectIds:
        for projId in projectIds:
            if projId and projId != "__CREATE__"and projId not in vendor.projectIds:
                    vendor.projectIds.append(projId)
                    project = get_project_from_db(projId)
                    if project:
                        project.vendorIds.append(vendorId)
                        project.put()
    vendor.put()
    time.sleep(1)
    return vendor

def delete_vendors_from_db():
    vendors = get_vendors_from_db(None)
    if vendors:
        for vendor in vendors:
            key = vendor.key
            if key:
                key.delete()

def get_criteria_average_from_calc(project, evaluation_criterion):
    entrys = get_entrys_from_given_project_db(project.projectId)
    total = len(entrys)
    if total > 0:
        current = 0.0
        for entry in entrys:
            for weight_splits in entry.weights:
                req_weight = weight_splits.split(":")
                if req_weight[0] == evaluation_criterion.evaluation_criterion:
                    current += float(req_weight[1])
        average = float (current / float(total))
    else:
        average = 0
    return average

def get_vendor_score_from_calc(project, evaluation_criterion, vendorId):
    entrys = get_entrys_from_given_project_db(project.projectId)
    score = 0
    ec = evaluation_criterion.evaluation_criterion.replace(" ", "^")
    key = vendorId + "^" + ec
    lene = len(entrys)
    for entry in entrys:
        if entry.vendor_output:
            vsplits = json.loads(entry.vendor_output)
            if key in vsplits:
                score += int(vsplits[key])
    if lene == 0:
        average_score = 0
    else:
        average_score = float(score/lene)
    return average_score

def get_business_objectives_from_db(projectId, withCalc):
    bos_db = []
    topVendor = None
    project = get_project_from_db(projectId)
    vendor_sums = {}
    for vendorId in project.vendorIds:
        vendor_sums[vendorId] = 0.0
    for objectiveId in project.objectiveIds:
        objective = get_objective_from_db(projectId, objectiveId)
        if objective:
            evaluation_criteriaIds = objective.evaluation_criteriaIds
            evaluation_criteria = []
            for evaluation_criteriaId in evaluation_criteriaIds:
                evaluation_criterion = get_evaluation_criteria_from_db(projectId, objectiveId, evaluation_criteriaId)
                if evaluation_criterion:
                    if withCalc:
                        calculations = {}
                        criteria_average= get_criteria_average_from_calc(project, evaluation_criterion)
                        criteria_weight = float(objective.weight * criteria_average)
                        calculations["criteria_percentage"] = criteria_average
                        calculations["criteria_weight"] = criteria_weight
                        for vendorId in project.vendorIds:
                            vendor_score = get_vendor_score_from_calc(project, evaluation_criterion, vendorId)
                            key = vendorId + "_vendor_score"
                            calculations[key] = vendor_score
                            vendor_weighted_score = float(vendor_score * criteria_weight)
                            key = vendorId + "_vendor_weighted_score"
                            calculations[key] = vendor_weighted_score
                            vendor_sums[vendorId] += vendor_weighted_score
                        evaluation_criterion.calculations = calculations
                    evaluation_criteria.append(evaluation_criterion)
            objective.evaluation_criteria = evaluation_criteria
            bos_db.append(objective)
    maxVal = 0
    for vendorId in project.vendorIds:
        if maxVal < vendor_sums[vendorId]:
            topVendor = vendorId
            maxVal = vendor_sums[vendorId]
    return bos_db, topVendor, vendor_sums

def check_auth(identity, password):
    """This function is called to check if a username /
        password combination is valid.
        """
    user = get_user_from_db(identity)
    if user:
        return True
    else:
        if identity == 'superuser' and password == 'password':
            update_user('superuser', 'superuser@lafoot.com', 'Superuser', 'password', None)
            time.sleep(1)
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
        #print "***** " + str(request.authorization)
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        else:
            return f(*args, **kwargs)

    return decorated

def checkIfAdminUser():
    user = get_user_from_db(request.authorization.username)
    if user.type == "User":
        return False
    else:
        return True
