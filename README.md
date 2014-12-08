# FACET Shift Report
This is a Flask app to handle FACET user shift reports.  FACET user groups will use the system to make a end-of-shift report, which will then get stored in a database, as well as posted to the FACET physics elog.

## Development
If you want to work on the project, it is pretty easy to do:  clone the repository, run 'pip install -r requirements.txt' in the directory to install the required python modules, then run 'python run.py' to start the development server.

## Deployment
Deploying on production should be pretty straightforward, if you are using Passenger to host python WSGI apps. Note that configuring Passenger isn't in the scope of this readme, you'll have to figure that one out on your own. Clone the repo, run 'pip install -r requirements.txt', set the 'FACETSHIFTREPORT_SETTINGS' environment variable to point to the 'config_prod.py' file included in the repo.  Add whatever settings you need to get production stuff working to config_prod.py, don't mess with the normal config.py unless you want the changes to apply to both development and production mode.