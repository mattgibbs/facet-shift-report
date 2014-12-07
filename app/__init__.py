from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('FACETSHIFTREPORT_SETTINGS')
db = SQLAlchemy(app)

from app import views, models