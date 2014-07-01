from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	reports = db.relationship('ShiftReport', backref = 'author', lazy = 'dynamic')
	
	def __repr__(self):
		return '<User Group %r>' % (self.name)

class ShiftReport(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	timestamp = db.Column(db.DateTime())
	body = db.Column(db.Text())
	elogurl = db.Column(db.Text())
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post %r>' % (self.body)