# sample-table

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

To run from command line.
cd to the folder where this repo is cloned/checked-out
<gae-directory>/google-cloud-sdk/bin/dev_appserver.py app.yaml
Point browser to http://localhost:8080/form
Select some check-boxes and Submit
