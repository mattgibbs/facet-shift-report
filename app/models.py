from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	reports = db.relationship('ShiftReport', backref = 'author', lazy = 'dynamic')
	
	def __init__(self, form):
		self.name = form.data['userName']
	
	def __repr__(self):
		return '<User Group %r>' % (self.name)

class ShiftReport(db.Model):
	id				= db.Column(db.Integer, primary_key = True)
	elogurl			= db.Column(db.Text())
	
	# Everything below exists on the Form
	user			= db.Column(db.Integer, db.ForeignKey('user.id'))
	shifts			= db.Column(db.String())
	personnel		= db.Column(db.Text())

	# USE DATETIME FORMAT OF %Y-%m-%dT%H:%M:%S FOR FILE NAME
	shiftStart		= db.Column(db.DateTime())
	shiftEnd		= db.Column(db.DateTime())

	goals			= db.Column(db.Text())
	progress		= db.Column(db.Text())
	problems		= db.Column(db.Text())
	nextShift		= db.Column(db.Text())
	briefSummary	= db.Column(db.Text())
	other			= db.Column(db.Text())

	usefulBeam		= db.Column(db.Integer)
	unschedAccDown	= db.Column(db.Integer)
	unschedUserDown	= db.Column(db.Integer)
	physAvail		= db.Column(db.Integer)

	def __init__(self, form):
		self.read_form(form)

	def read_form(self, form):
		self.user 				= form.data['user']
		self.shifts				= form.data['shifts']
		self.personnel			= form.data['personnel']
		self.shiftStart			= form.data['shiftStart']
		self.shiftEnd			= form.data['shiftEnd']
		self.goals				= form.data['goals']
		self.progress			= form.data['progress']
		self.problems			= form.data['problems']
		self.nextShift			= form.data['nextShift']
		self.briefSummary		= form.data['briefSummary']
		self.other				= form.data['other']
		self.usefulBeam			= form.data['usefulBeam']
		self.unschedAccDown		= form.data['unschedAccDown']
		self.unschedUserDown	= form.data['unschedUserDown']
		self.physAvail			= form.data['physAvail']
	def __repr__(self):
		return '<Post by %r>' % (self.user)