CSRF_ENABLED = True
SECRET_KEY = 'jvryailvnbclafdsailrna'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
# if hostname == ad-ops* or something, use postgres
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')