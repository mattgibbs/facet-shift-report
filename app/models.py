from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class ShiftReport(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	