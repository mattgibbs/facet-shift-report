from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')
try:
	os.environ["FACETSHIFTREPORT_SETTINGS"]
	app.config.from_envvar('FACETSHIFTREPORT_SETTINGS')
	print "Running in production mode."
except KeyError:
	print "Running in development mode."
	

db = SQLAlchemy(app)

from app import views, models