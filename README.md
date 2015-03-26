# FACET Shift Report
This is a Flask app to handle FACET user shift reports.  FACET user groups will use the system to make a end-of-shift report, which will then get stored in a database, as well as posted to the FACET physics elog.

## Development
If you want to work on the project, it is pretty easy to do:

1.  Clone the repository, run 'pip install -r requirements.txt' in the directory to install the required python modules.
2.  In the same directory as app.py, make a file called 'secrets.py'.  Inside the file, assign an '`admin_username`' variable and an '`admin_password`' variable.  The full contents of secrets.py should look like this:
	
		admin_username = "admin"
		admin_password = "password"
	
	secrets.py isn't saved in the repository for obvious security reasons.
3.  Run 'python app.py db upgrade' to initialize the database.
4.  Run 'python run.py' to start the development server.

## Deployment
Deploying on production should be pretty straightforward, if you are using Passenger to host python WSGI apps. Note that configuring Passenger isn't in the scope of this readme, you'll have to figure that one out on your own.

1.  Clone the repo, run 'pip install -r requirements.txt'.
2.  Set the 'FACETSHIFTREPORT\_SETTINGS' environment variable to point to the 'config\_prod.py' file included in the repo.  Add whatever settings you need to get production stuff working to config\_prod.py, don't mess with the normal config.py unless you want the changes to apply to both development and production mode.
3.  Make a secrets.py file to set up an admin username and password.  See Item #2 in the 'Development' section of this document.
4.  Run 'python app.py db upgrade' to initialize the database.
