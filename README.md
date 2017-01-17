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
 - UI Perk ups

Example Input:

![Example Input](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Input.png)

Example Output:

![Example Output](https://raw.githubusercontent.com/paddyvishnubhatt/sample-table/master/misc/Output.png)
