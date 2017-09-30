# Demo DAR

Demo steps:
----------

1. Start server:
 1. Either in GAE using GAE deployment scripts (will need an account - most likely the demo will be well within Free tier)
 2. Local : ~/tools/google-cloud-sdk/platform/google_appengine/dev_appserver.py app.yaml
 ![Run Server](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/RunServer.png)
 
2. Create Admin users: Point your phone/ipad/browser(private or incognito) to the URL from above (either the appspot from GAE or localhost)
  1. ~/<url>:8080/
  2. Seed the DB w/ admin password. Login as Superuser (admin/password)
  ![Superuser Login](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/SuperuserLogin.png)

  3. Create the first Project's admin user.
    1. user1 (enter details and submit)
![Create Admin User](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/User.png)

3. Create Project: Use another device/browser (private or incognito) and again point to the URL from GAE (or localhost)
  1. ~/<url>:8080/ 
  2. Login using the admin password created in above step
![Admin Login](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/AdminLogin.png)
 
  3. Create a project and enter details.
 ![Create Project](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Project.png)
  
  4. Create more users (regular users)
 ![Create Regular User](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/User.png)
 
  5. Create entry as admin
  ![Create Entry](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Entry.png)

4. Create User Entries: Use another device/browser (private or incognito) and again point to the URL from GAE (or localhost)
  1. ~/<url>:8080/ 
  2. Login using the user password created in above step
![Admin Login](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/UserLogin.png)
  
  3. Create entries
  4. Repeat this for as many users created in the above step
  ![Create Entry](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Entry.png)

5. Review Summary: Use the same device/browser (private or incognito) from Step 3, again point to the URL from GAE (or localhost)
  1. ~/<url>:8080/ 
  2. Login using the admin user/password
  3. Review the Summary pages/entries from all users
  ![Summary of Entrys](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Entrys.png)

6. To repeat - lather/rinse/repeat - Clean up (delete) all data from GAE data store and restart.
