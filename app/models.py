from app import db
from flask import url_for
import physicslog
import archiver
import time

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	experiment_title = db.Column(db.String(140))
	reports = db.relationship('ShiftReport', backref = 'author', lazy = 'dynamic')
	
	def read_form(self, form):
		self.name = form.data['userName']
		self.experiment_title = form.data['experiment_title']
	
	def __init__(self, form=None):
		if form:
			self.read_form(form)
	
	def __repr__(self):
		if self.experiment_title:
			return '%s - %s' % (self.name, self.experiment_title)
		return self.name

class ShiftReport(db.Model):
	id				= db.Column(db.Integer, primary_key = True)
	elogurl			= db.Column(db.Text()) # Edit when we write our entry to the elog.
	
	# Everything below exists on the Form
	user			= db.Column(db.Integer, db.ForeignKey('user.id'))
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

	usefulBeam		= db.Column(db.Float)
	unschedAccDown	= db.Column(db.Float)
	unschedUserDown	= db.Column(db.Float)
	physAvail		= db.Column(db.Float)
	requested_time = db.Column(db.Float)
	
	usesPositrons = db.Column(db.Boolean, default = False)
	numParticles = db.Column(db.Float)
	numParticles_sigma = db.Column(db.Float)
	x_rms_li20 = db.Column(db.Float)
	x_rms_li20_sigma = db.Column(db.Float)
	y_rms_li20 = db.Column(db.Float)
	y_rms_li20_sigma = db.Column(db.Float)
	bunch_length = db.Column(db.Float)
	bunch_length_sigma = db.Column(db.Float)
	
	hidden = db.Column(db.Boolean())
	submitted = db.Column(db.Boolean(), default = False)
	logbook_entry_url = db.Column(db.String(140))

	def __init__(self, form=None):
		self.hidden = False
		if form:
			self.read_form(form)
	
	def totalHours(self):
		try:
			return self.unschedUserDown + self.usefulBeam + self.unschedAccDown
		except TypeError:
			return 0.0
	
	def physAvailPercentage(self):
		if self.totalHours() > 0:
			return "{0}%".format(int((self.physAvail / self.totalHours()) * 100))
		return "Not Available"

	def read_form(self, form):
		self.user 				= str(form.data['user']) # Form uses strings. I don't think you can pair int/str in the choices
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
		self.usesPositrons = (form.data['usesPositrons'] == "True")
		self.numParticles = form.data['numParticles']
		self.x_rms_li20 = form.data['x_rms_li20']
		self.y_rms_li20 = form.data['y_rms_li20']
		self.bunch_length = form.data['bunch_length']
		self.usefulBeam			= form.data['usefulBeam']
		self.unschedAccDown		= form.data['unschedAccDown']
		self.unschedUserDown	= form.data['unschedUserDown']
		self.physAvail			= form.data['physAvail']
		self.requested_time = form.data['requested_time']
	def __repr__(self):
		return '<Post by %r>' % (self.user)
  
	def get_archived_beam_parameters(self):
		(self.numParticles, self.numParticles_sigma) = archiver.get_mean_and_std('LI20:TORO:2040:DATA', self.shiftStart, self.shiftEnd)
		self.numParticles = self.numParticles / 1.0E10
		self.numParticles_sigma = self.numParticles_sigma / 1.0E10
		(self.x_rms_li20, self.x_rms_li20_sigma) = archiver.get_mean_and_std('WIRE:LI20:3206:XRMS', self.shiftStart, self.shiftEnd)
		(self.y_rms_li20, self.y_rms_li20_sigma) = archiver.get_mean_and_std('WIRE:LI20:3206:YRMS', self.shiftStart, self.shiftEnd)
		(self.bunch_length, self.bunch_length_sigma) = archiver.get_mean_and_std('PROF:LI20:3230:BLEN', self.shiftStart, self.shiftEnd)
		
	
	
	def post_to_logbook(self):
		entry = physicslog.Entry()
		entry.title = unicode("FACET User Summary for {0} to {1}").format(self.shiftStart.strftime("%Y-%m-%d %H:%M"), self.shiftEnd.strftime("%Y-%m-%d %H:%M"))
		entry.author = unicode(self.author.name)
		entry.text = unicode("__Experiment:__ {0} \r\n" + 
					"__Personnel:__ {1} \r\n" +
					"__Shift Start:__ {2} \r\n" +
					"__Shift End:__ {3} \r\n\r\n" +
					"__Goals:__\r\n{4}\r\n\r\n" +
					"__Progress:__\r\n{5}\r\n\r\n" +
					"__Problems:__\r\n{6}\r\n\r\n" +
					"__To Do Next Shift:__\r\n{7}\r\n\r\n" +
					"__Brief Summary:__\r\n{8}\r\n\r\n" +
					"__Other Notes:__\r\n{9}\r\n\r\n" +
					"__Particle Type:__ {15}\r\n" +
					"__Bunch Charge:__ {16}{20}  x10^10 particles\r\n" +
					"__LI20 Horizontal Beam Size:__ {17}{21} um\r\n" +
					"__LI20 Vertical Beam Size:__ {18}{22} um\r\n" +
					"__Bunch Length:__ {19}{23} um\r\n" +
					"| Useful Beam Time | Accelerator Downtime | User Downtime | Acc Physics Available \r\n" +
					"| {10} | {11} | {12} | {13} \r\n\r\n" + 
					"View this report in the FACET Shift Reports system: {14}").format(self.author, self.personnel, self.shiftStart, self.shiftEnd,
														self.goals, self.progress, self.problems, self.nextShift,
														self.briefSummary, self.other, self.usefulBeam,
														self.unschedAccDown, self.unschedUserDown, self.physAvail,
														url_for('view_report', reportid=self.id, _external=True),
														"Positrons" if self.usesPositrons else "Electrons",
														round(self.numParticles,2) if self.numParticles else None,
														round(self.x_rms_li20,2) if self.x_rms_li20 else None,
														round(self.y_rms_li20,2) if self.y_rms_li20 else None,
														round(self.bunch_length,2) if self.bunch_length else None,
														" +/- " + str(round(self.numParticles_sigma,2)) if self.numParticles_sigma else '',
														" +/- " + str(round(self.x_rms_li20_sigma,2)) if self.x_rms_li20_sigma else '',
														" +/- " + str(round(self.y_rms_li20_sigma,2)) if self.y_rms_li20_sigma else '',
														" +/- " + str(round(self.bunch_length_sigma,2)) if self.bunch_length_sigma else '')
		entry.timestamp = self.postTime
		success_status = entry.submit("facetelog")
		return success_status