# sample-table

1/14/2017:
---------
Project is on Google appengine
Needs a google / gcloud project and ID
Populate project id (right now set to 'shenba') in app.yaml with it.

- Description of files
 - static/ -> css 
 - templates/ -> html files to input the form and ouput of selections from form
 - table.html uses a table
 - main.py -> the code to input form and output
 - get_requirements is where the requirement is built - this must be changed to have more examples
  - this is meant to take arbitrary requirements
  - the requirements is rendered in / by table.html
  - the form is inputt-ed in table.html and the output is taken into submitted_table.html

Edited/built using pycharm 2016.3.2

- To run from command line.
- cd to the folder where this repo is cloned/checked-out
- <gae-directory>/google-cloud-sdk/bin/dev_appserver.py app.yaml
- Point browser to http://localhost:8080/form
- Select some check-boxes and Submit

1/16/2017:
---------
 - Add persistence
   - Use Google data store
   - Create a template for Register - this contains the requirements fields to be displayed in the table.
   - For now create a singleton and store in DB (called SingletonRegister) and use this
   - If one exists - use it for Entrys, if not create a hard-coded one for now. Register contains
     - A name/ID
     - Requirements list (e.g. size, cost, smartapps)
     - Users list
   - Create Entrys using the form. Each Entry contains
     - Back pointer to the Register where it is derived/built from
     - Author - user/author who created this entry
     - Date when entered/created
     - requirements as selected by the user/author
   - Create Users with the Registers - these are the allowed users. 
     - For now create the users within the singleton
 - Add API and bare-bone/basic UI
   - /register-debug/<registerId>
    - For now read-only and debug - show the singleton 
      - Json only
   - / or /show_registers
    - Display list of Registers
      - If none exists, create a Singleton default 
    - For now allow selection of singleton 
     - Upon selecting register (<registerId>)
      - /show_register/<registerId> -> display register details
      - /show_entrys/<registerId> -> display existing, current entries from diff users
        - Upon selecting an entry - show details
      - /form_entry/<registerId> -> launch form_entry for the register
      - /form_entry/<registerId>
        - Given a register, it should display the table for the user to pick
        - Select (force) a user
        - Submit will create the form entry 
      - /show_users/<registerId> -> display users
        - Upon selecting a user 
          - /show_user/<user> -> display user details
      - /create_register -> Create a new register
      - /create_user -> Create new user
      - /edit_users -> 

1/17/2017
---------
 - Clean up code, models
  - Use CRUD functions and model APIs around that for
    - Register
    - User
    - Requirements - right now this is a list - make this an object on its own.
    - Entry(s)
 - UI Perk ups
 
List of all Registers.
  - This lists all the existing registers and also has a link to create a new one
  - Register contains
    - Name/ID
    - Users to enter forms
    - Requirements list
  - Create Register allows to create a new one w/ above attributes
   - Upon creating a register - it comes back w/ a screen w/ what was created
   - From here you can also create users in the system and associate them to the Register
    - Upon creating a user - it comes back w/ a screen w/ what was created
    - You can also edit user list associated w/ a Requirement
  - For each Register - you can perform the following actions on that (from above screen)
   - List form entries 
     - Clicking on entry shows details of each Entry - they being:
      - User who created it
      - Date when created
      - Requirements selected by/for this entry
     - Create a new Entry
      - This will force a user to be selected - if not the default is chosen
      - Creates an entry
       - Upon creating a entry - it comes back w/ a screen w/ what was created
 
 Schema: There're three abstractions. Pls review and help augment if anything needed
  - Register
  - User
  - Entry
  - Requirements is flat list of strings

Deletes - are not available. But you should use the database viewer running port 8000 to list entities of each kind of class (Register, User, Entry)

The code - Mainly three files and one folder:
- main.py -> this is the views - it has the webservice/REST end-points, url-routing and View logic integration w/ models
- register.py -> models
- utils.py -> db access layer
- templates folder -> jinja2 based which have logic to parse the models sent by main.py to display
- Rest is all ancilliary for/from gae, flask, etc

01/18/2017
----------
Now there's Auth layer to force users to login
- Three kinds of users
 - Admin - who can set / create / update Registers view Forms for all, etc
 - User - who can enter forms and review/edit their own entries
 - Superuser is admin/password (backdoor still kept open)
 - Note: if auth fails - no api will work
- The work flow is:
- Using SuperUser admin/password user will create the Registers
- Once registers are created - users will be created along with that
- Some users will be Admin - some regular/Users
- Every screen is now auth protected (using basic auth model)
- Every register has a default password, when users are created for a register- they all inherit the same defaultPassword
- Right now register and user are tied - one user should be able to create form/entrys for more than one requirement/register - i don't think this is feasible.

01/19/2017:
-----------
- Start from clean slate
- Login as superuser - admin/password
- This will land you in the users screen, where you can add Admin users
 - Organize one admin per project (register)
- Login as admin user as created above (if on chrome - use incognito or private-viewing in firefox)
 - When logged in as admin, you can 
  - Create Project
  - Create more users (regular User)
- Now Login as regular user (use another browser or clear data from browser)
 - When logged in as user, you can 
  - Create one entry
  - Repeat steps 7,8 with more/different users
- Login back as admin - 
 - view the registers, 
 - entrys per register, 
 - users per register
- Ancilliary functions
 - Edit Register
 - Update requirements
 - Update Users
 - Edit User
- Next todo:
 - Wire up the summary and requirement analyses code (write a simple python code as functions and call them
 - Present the results in a summary-page/project as a view
- Future Todo:
 - Once a register/requirement is defined - it cannot or should not be allowed to modify if there're user entrys - else it will make modeling and your summary calcs difficult
 - Introduce versioning of Register or requirements in Register or user has to create new Register for each modified/new set of Requirements

01/21/2017:
-----------
Demo steps described in Demo.md

1/24/2017:
---------
1. Added validate function in javascript code based on the python brute force function in test_sort.py
2. This needs work.
3. The code to calculate prioritized list is in a function called validate() in entry.html
4. Run the app locally - as before.
5. Launch browser - if chrome - open the Javascript console. 
6. When you select check boxes and change selections, enable the Show Calc cb and observe the output in the console.
7. You can make changes to the validate function too - i.e. fix code or add more console logs - when you do this - change the code and refresh.

01/26/2017:
----------
1. To calculate the total possible/expected tuples: If N is number of requirements, then number of tuples = (n square - n) / 2
2. Subtotal = # of 1s in the column
3. Weight = Subtotal / <The total # of 1s in the sheet>
4. Across all users - Add the weights of R1 and divide by # of users

02/15/2017:
----------
There's a list of projects, Each project has
1. id
2. due date
3. Vendors - is this a constant list or different for diff project? Because item below (1.2.7.5.5 and 1.2.7.5.7) depend upon this - i have to draw up as many columns as there are vendors. 
4. users (at least one admin)
5. and Its housekeeping info (name, desc, etc)
6. List of business objectives, Each objective has
  1. id
  2. description
  3. weight     <-------- Entered manually by each (admin) user on a scale of 1-5
  4. List of Evaluation criteria, Each eval criteria has
    1. id
    2. evaluation criterion
    3. criteria % age  <--- Obtained from the forced pair ranking. This is the summary calculate weight for each column coming from each (user) user
    4. weight (which is to be calculated)
    5. option 1 score <--- This is actually the score for Vendor 1. Entered manually by each (admin) user - value of Yes, No, Maybe
weighted score(calculated)
    6. option 2 score <--- This is actually the score for Vendor 2. Entered manually by each (admin) user - value of Yes,No,Maybe
weighted score (calculated)
    7. There might be more options (i.e vendors)
7. Based on the items 2 - uild a tabular screen w/ dialogs to enter new objectives, new eval criteria
8. Entry Forms for Users - 
9. Flow:
  1. User logs in and is taken to their list of projects
  2. User selects project
  3. User then selects business objective
  4. Upon selecting the bus obj - user will then get the same table as before for evaluation criteria (used to be called requirements)
  5. User enters - for each user calculations are performed and a summary will be rolled up to the project level to feed into the above data.
  Q: Does the (user) user see vendors and have any input for vendor/options?
  Yes, each user has to enter YES/NO/MAYBE for each evaluation criteria for each vendor.


