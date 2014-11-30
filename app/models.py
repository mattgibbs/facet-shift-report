from app import db
import physicslog
import time

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	reports = db.relationship('ShiftReport', backref = 'author', lazy = 'dynamic')
	
	def __init__(self, form=None):
		if form:
			self.name = form.data['userName']
	
	def __repr__(self):
		return '<User Group %r>' % (self.name)

class ShiftReport(db.Model):
	id				= db.Column(db.Integer, primary_key = True)
	elogurl			= db.Column(db.Text()) # Edit when we write our entry to the elog.
	
	# Everything below exists on the Form
	user			= db.Column(db.Integer, db.ForeignKey('user.id'))
	shifts			= db.Column(db.String())
	personnel		= db.Column(db.Text())

	# USE DATETIME FORMAT OF %Y-%m-%dT%H:%M:%S FOR FILE NAME
	postTime		= db.Column(db.DateTime())
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

	def __init__(self, form=None):
		if form:
			self.read_form(form)

	def read_form(self, form):
		self.user 				= str(form.data['user']) # Form uses strings. I don't think you can pair int/str in the choices
		self.shifts				= form.data['shifts']
		self.personnel			= form.data['personnel']
		self.postTime			= form.data['postTime']
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
        
	def post_to_logbook(self):
		entry = physicslog.Entry()
		entry.title = "FACET User Summary for {0} Shift".format(self.shifts)
		entry.author = self.author.name
		entry.text = ("__User:__ {0} \r\n" + 
					"__Shift Start:__ {1} \r\n" +
					"__Shift End:__ {2} \r\n" +
					"__Goals:__ {3} \r\n" +
					"__Progress:__ {4} \r\n" +
					"__Problems:__ {5} \r\n" +
					"__To Do Next Shift:__ {6} \r\n" +
					"__Brief Summary:__ {7} \r\n" +
					"__Other:__ {8} \r\n" +
					"| Useful Beam Time | Accelerator Downtime | User Downtime | Acc Physics Available \r\n" +
					"| {9} | {10} | {11} | {12}").format(self.author.name, self.shiftStart, self.shiftEnd,
														self.goals, self.progress, self.problems, self.nextShift,
														self.briefSummary, self.other, self.usefulBeam,
														self.unschedAccDown, self.unschedUserDown, self.physAvail)
		entry.timestamp = self.postTime
		entry.submit("facetelog")