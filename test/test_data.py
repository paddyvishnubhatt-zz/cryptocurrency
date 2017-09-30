import requests
import base64
import time
import json

URL = "http://localhost:8080"
num_users = 3

#URL = "http://daranalysis-200000.appspot.com"
#num_users = 10

def create_users():
    url = URL + "/api/v1/submitted_user"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    userIds = []
    for u_idx in range(0, num_users):
        form_params = {}
        if u_idx == 1:
            userId = "Admin"
            form_params["identity"] = userId
            form_params["type"] = "Admin"
        else:
            userId = "User-" + "-" + str(u_idx)
            form_params["identity"] = userId
            form_params["type"] = "User"
        form_params["email"] = userId + "@crytocurrency.com"
        form_params["password"] = "defaultPassword"
        requests.post(url,
                      data=form_params,
                      headers={"Authorization": "Basic %s" % b64Val})
        userIds.append(userId)
    return userIds

def delete_users():
    url = URL + "/api/v1/delete_users"
    usrPass = "superuser:password"
    b64Val = base64.b64encode(usrPass)
    response = requests.delete(url,
                               headers={"Authorization": "Basic %s" % b64Val})

def main():
    create_users()
    #delete_users()

if __name__ == "__main__":
    main()