import urllib
import urllib2
import urlfetch
import json

firebase_server_key = "key=AIzaSyDxwE1m7WjI6400WD9GadNJqoZfJvBmjGs"
fcm_server = "https://fcm.googleapis.com/fcm/send"
fcm_headers = {"Content-type": "application/json", "Authorization" : firebase_server_key}

title = "DAR Entry Reminder: Your DAR entry needs to completed"
content = "Hello Paxton, You have to work on your DAR Entrys on project: Project-Management "
toaddr = "ejDCPChiP2Q:APA91bE31WkfZsDj3n0Wb4Hju-pEP19Whx0WSqdRFgZSkpdVc4F2Nnl5AJDT8kFOU1S1dBewOCSVAwRDbkSWv-JB9wnqG9Lq0qHpPi0V7PPxd1DH7ydmjCIklsGkhnXJF6hc-ld6TRHe"
headers = fcm_headers
url = fcm_server

data = {'priority': 'high', 'to': toaddr, 'notification' : {'badge': '1', 'sound' : 'default', 'title' : title, 'body' : content}}

#resp = urlfetch.fetch( url, headers=headers, method="POST", payload=urllib.urlencode(data))
#print resp.content

try:
    opener = urllib2.build_opener()
    req = urllib2.Request(url, data=json.dumps(data), headers=headers)
    resp = opener.open(req)
except urllib2.HTTPError as e:
    error_message = e.read()
    print error_message

