import requests
import base64
import time

URL = "http://localhost:8080"
num_projects = 5
num_users = 5
num_requirements = 4
num_entrys = num_users

def post_users(projectId):
    url = URL + "/api/v1/submitted_user"
    usrPass = "admin:password"
    b64Val = base64.b64encode(usrPass)
    userIds = []
    for u_idx in range(1, num_users):
        form_params = {}
        if u_idx == 1:
            userId = "Admin-" + projectId
            form_params["identity"] = userId
            form_params["type"] = "Admin"
        else:
            userId = "User-" + projectId + "-" + str(u_idx)
            form_params["identity"] = userId
            form_params["type"] = "User"

        form_params["email"] = userId + "@sellerforce.com"
        form_params["password"] = "defaultPassword"
        form_params["projectId"] = projectId
        response = requests.post(url,
                                 data=form_params,
                                 headers={"Authorization": "Basic %s" % b64Val})
        #print response.content
        userIds.append(userId)
    return userIds

def post_projects():
    url = URL + "/api/v1/submitted_project"
    for p_idx in range (1,num_projects):
        form_params = {}
        projectId = "Project-" + str(p_idx)
        form_params["projectId"] = projectId
        form_params["department"] = "Department-Q"
        form_params["group"] = "lawn-mowers"
        form_params["description"] = "This requirement is for lawn mowers but could be applied to dish washers also"
        form_params["defaultPassword"] = "test1234"
        requirement_items = ""
        first = True
        for r_idx in range(1, num_requirements):
            if first:
                first = False
                requirement_items += "Req-" + projectId + "-" + str(r_idx)
            else:
                requirement_items += "," + "Req-" + projectId + "-" + str(r_idx)
        form_params["requirements"] = requirement_items
        form_params["userIds[]"] = post_users(projectId)
        time.sleep(1)
        usrPass = "Admin-"+projectId+":defaultPassword"
        b64Val = base64.b64encode(usrPass)
        response = requests.post(url,
                                 data=form_params,
                                 headers={"Authorization": "Basic %s" % b64Val})
        print projectId

def post_entrys():
    iurl = URL + "/api/v1/submitted_entry"
    for p_idx in range(1,num_projects):
        projectId = "Project-" + str(p_idx)
        url = iurl + "/" + projectId
        for e_idx in range(1,num_entrys):
            form_params = {}
            if e_idx == 1:
                userId = "Admin-" + projectId
            else:
                userId = "User-" + projectId + "-" + str(e_idx)
            usrPass = userId + ":defaultPassword"
            b64Val = base64.b64encode(usrPass)

            number = 0
            form_params = {}
            for req_idx1 in range(1, num_requirements):
                for req_idx2 in range(1, num_requirements):
                    if req_idx1 != req_idx2:
                        req_idx = "Req-" + projectId + "-" + str(req_idx1) + "_" + "Req-" + projectId + "-" + str(req_idx2)
                        if number % 2 == 0:
                            switch_req = "Req-" + projectId + "-" + str(req_idx2) + "_" + "Req-" + projectId + "-" + str(req_idx1)
                            if switch_req not in form_params:
                                form_params[req_idx] = "True"
                    number += 1

            response = requests.post(url,
                                     data = form_params,
                                     headers={"Authorization": "Basic %s" % b64Val})
            print projectId

def delete_projects():
    url = URL + "/api/v1/delete_project"
    for p_idx in range (1,num_projects):
        projectId = "Project-" + str(p_idx)
        usrPass = "Admin-"+projectId+":defaultPassword"
        b64Val = base64.b64encode(usrPass)
        response = requests.delete(url + "/" + projectId,
                                 headers={"Authorization": "Basic %s" % b64Val})
        print projectId
        time.sleep(1)

def delete_users():
    url = URL + "/api/v1/delete_users"
    usrPass = "admin:password"
    b64Val = base64.b64encode(usrPass)
    response = requests.delete(url,
                               headers={"Authorization": "Basic %s" % b64Val})


if __name__ == "__main__":
    post_projects()
    post_entrys()
    #delete_projects()
    #delete_users()