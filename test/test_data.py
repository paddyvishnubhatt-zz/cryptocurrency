import requests
import base64
import time
import json
from datetime import timedelta
import datetime

URL = "http://localhost:8080"
num_projects = 2
num_users = 3
num_vendors = 3
num_entrys = num_users
BOS=[u'{"objectiveId":"objective1","description":"this is objective1","weight":"1",'
                                u'"evaluation_criteria":[{"evaluation_criterionId":"1","evaluation_criterion":"criterion 1"},'
                                u'{"evaluation_criterionId":"2","evaluation_criterion":"criterion 2"},'
                                u'{"evaluation_criterionId":"3","evaluation_criterion":"criterion 3"}]},'
                                u'{"objectiveId":"objective2","description":"this is objective2","weight":"2",'
                                u'"evaluation_criteria":[{"evaluation_criterionId":"4","evaluation_criterion":"criterion 4"},'
                                u'{"evaluation_criterionId":"5","evaluation_criterion":"criterion 5"},'
                                u'{"evaluation_criterionId":"6","evaluation_criterion":"criterion 6"}]}']

def post_vendors(projectId):
    url = URL + "/api/v1/submitted_vendor"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    vendorIds = []
    for v_idx in range(0, num_vendors):
        form_params = {}
        vendorId = "V-" + projectId + "-" + str(v_idx)
        form_params["identity"] = vendorId
        form_params["email"] = vendorId + "@" + vendorId + ".com"
        form_params["projectId"] = projectId
        vendorIds.append(vendorId)
        requests.post(url,
                      data=form_params,
                      headers={"Authorization": "Basic %s" % b64Val})
    return vendorIds

def post_users(projectId):
    url = URL + "/api/v1/submitted_user"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    userIds = []
    for u_idx in range(0, num_users):
        form_params = {}
        if u_idx == 1:
            userId = "Ad-" + projectId
            form_params["identity"] = userId
            form_params["type"] = "Admin"
        else:
            userId = "Us-" + projectId + "-" + str(u_idx)
            form_params["identity"] = userId
            form_params["type"] = "User"
        form_params["email"] = userId + "@sellerforce.com"
        form_params["password"] = "defaultPassword"
        form_params["projectIds"] = projectId
        requests.post(url,
                      data=form_params,
                      headers={"Authorization": "Basic %s" % b64Val})
        userIds.append(userId)
    return userIds

def post_projects():
    url = URL + "/api/v1/submitted_project"
    for p_idx in range (0,num_projects):
        form_params = {}
        projectId = "Proj-" + str(p_idx)
        form_params["projectId"] = projectId
        form_params["due_date"] = "2017-02-12"
        form_params["department"] = "Department-Q"
        form_params["group"] = "lawn-mowers"
        form_params["description"] = "This requirement is for lawn mowers but could be applied to dish washers also"
        form_params["defaultPassword"] = "test1234"
        form_params["bos[]"] = BOS
        form_params["userIds[]"] = post_users(projectId)
        form_params["vendorIds[]"] = post_vendors(projectId)
        time.sleep(1)
        usrPass = "Ad-"+projectId+":defaultPassword"
        b64Val = base64.b64encode(usrPass)
        response = requests.post(url,
                                 data=form_params,
                                 headers={"Authorization": "Basic %s" % b64Val})
        print projectId

def getArrayOfDict(bos):
    # this is not good
    bot = bos[0]
    # this is even worse
    bot = '[' + bot + ']'
    bol = json.loads(bot)
    return bol

def post_entrys():
    iurl = URL + "/api/v1/submitted_entry"
    bol = getArrayOfDict(BOS)
    ecs = []
    for bo in bol:
        ecb = []
        for ec in bo["evaluation_criteria"]:
            ecb.append(ec["evaluation_criterion"])
        ecs.append(ecb)
    for p_idx in range(0,num_projects):
        projectId = "Proj-" + str(p_idx)
        url = iurl + "/" + projectId
        for e_idx in range(0 ,num_entrys):
            if e_idx == 1:
                userId = "Ad-" + projectId
            else:
                userId = "Us-" + projectId + "-" + str(e_idx)
            usrPass = userId + ":defaultPassword"
            b64Val = base64.b64encode(usrPass)
            number = 0
            form_params = {}
            vendor_output = {}
            ec_output = []
            sub_total_col = {}
            num_checked = 0
            for ecb in ecs:
                for ec in ecb:
                    for v_idx in range(0, num_vendors):
                        vendorId = "V-" + projectId + "-" + str(v_idx)
                        key = vendorId + "^" + ec.replace(" ", "^")
                        vendor_output[key] = 0
                    for ec1 in ecb:
                        if ec != ec1:
                            req_idx = ec.replace(" ", "^") + "_" + ec1.replace(" ", "^")
                            if number % 2 == 0:
                                switch_req_idx = ec1.replace(" ", "^") + "_" + ec.replace(" ", "^")
                                if switch_req_idx not in form_params:
                                    form_params[req_idx] = "True"
                                    ec_output.append(req_idx)
                                    if ec in sub_total_col:
                                        sub_total_col[ec] = int(sub_total_col[ec]) + 1
                                    else:
                                        sub_total_col[ec] = 1
                                    num_checked += 1
                        else:
                            vendor_output[ec] = 0
                        num = 0
                        for v_idx in range(0, num_vendors):
                            vendorId = "V-" + projectId + "-" + str(v_idx)
                            key = vendorId + "^" + ec.replace(" ", "^")
                            if num % 2 == 0:
                                vendor_output[key] = 2
                            elif num % 2 == 0 and number % 2 == 0:
                                vendor_output[key] = 1
                            num += 1
                        number += 1
            form_params["evaluation_criteria_input"] = BOS
            form_params["evaluation_criteria_output"] = ec_output
            form_params["vendor_output"] = json.dumps(vendor_output)
            weights = {}
            for ec1 in sub_total_col:
                st = sub_total_col[ec1]
                weight_col = round(float (float(st)/ float(num_checked)),2)
                weights[ec1] = weight_col
            form_params["weights"] = json.dumps(weights)
            response = requests.post(url,
                                     data = form_params,
                                     headers={"Authorization": "Basic %s" % b64Val})
            print str(response) + " " + userId + ", " + projectId

def delete_projects():
    url = URL + "/api/v1/delete_project"
    for p_idx in range (0,num_projects):
        projectId = "Proj-" + str(p_idx)
        usrPass = "superuser:password"
        b64Val = base64.b64encode(usrPass)
        response = requests.delete(url + "/" + projectId,
                                 headers={"Authorization": "Basic %s" % b64Val})
        print projectId
        time.sleep(1)

def delete_users():
    url = URL + "/api/v1/delete_users"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    response = requests.delete(url,
                               headers={"Authorization": "Basic %s" % b64Val})
def delete_vendors():
    url = URL + "/api/v1/delete_vendors"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    response = requests.delete(url,
                               headers={"Authorization": "Basic %s" % b64Val})

if __name__ == "__main__":
    post_projects()
    post_entrys()
    #delete_projects()
    #delete_users()
