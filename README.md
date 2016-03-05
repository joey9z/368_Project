# 368_Project
Project for ECE 368, an automatic class scheduler for Purdue ECE classes

It's hosted on [Google App Engine](https://cloud.google.com/appengine/docs/python/)

The application is accessible at: http://ece-degree-builder.appspot.com/

The api output is accessible at: http://ece-degree-builder.appspot.com/api/

#src Folder

Contains the application source code

## Data Folder

### index.html

An example HTML file with the Bootstrap CSS Framework added. It contains markup for a simple HTML form.

### purdue_catalog.html

An HTML file containing course information page links and a short description for every Purdue course. The course links from this file will need to be parsed out to retrieve the course pages.

### prerequisites.js

Contains a node.js file with some previous regex work on parsing the prerequisite data from a course page.
