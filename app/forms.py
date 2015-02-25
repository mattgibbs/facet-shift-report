from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from app import models
from datetime import datetime

class UserForm(Form):
	userName		= fields.TextField('Experiment name', validators = [Required()])
	experiment_title = fields.TextField('Experiment title', validators = [Required()])
	def read_user(self, user):
		self.userName.data = str(user.name)
		self.experiment_title.data = str(user.experiment_title)

class ShiftForm(Form):
	user 			= fields.SelectField('Experiment', choices=[('error', 'FAILED TO LOAD EXPERIMENTS')], validators=[Required()], default=0)
	personnel		= fields.TextAreaField('Shift Leader/Shift Personnel')

	# USE DATETIME FORMAT OF %Y-%m-%dT%H:%M:%S FOR FILE NAME
	postTime		= fields.DateTimeField('Time to Post to E-Log', default=datetime.now, format="%Y-%m-%d %H:%M:%S", validators=[Required()])
	shiftStart		= fields.DateTimeField('Shift Start Time', default=datetime.now, format="%Y-%m-%d %H:%M:%S", validators=[Required()])
	shiftEnd		= fields.DateTimeField('Shift End Time', default=datetime.now, format="%Y-%m-%d %H:%M:%S", validators=[Required()])

	goals			= fields.TextAreaField('Goals')
	progress		= fields.TextAreaField('Progress')
	problems		= fields.TextAreaField('Problems')
	nextShift		= fields.TextAreaField('To Do On Next Shift')
	briefSummary	= fields.TextAreaField('Brief Summary', validators = [Required()])
	other			= fields.TextAreaField('Other Notes')

	requested_time = fields.DecimalField('Beam Time Requested')
	usefulBeam		= fields.DecimalField('Useful Beam Time')
	unschedAccDown	= fields.DecimalField('Unscheduled Accelerator Downtime')
	unschedUserDown	= fields.DecimalField('Unscheduled User Downtime')
	physAvail		= fields.DecimalField('Accelerator Physics Group Support Available')
	requested_time = fields.DecimalField('Beam Time Requested')
	''' Unsure how I want to add the following:
	s2chargeDeliv	= fields.DecimalField('')
	s2chargeReq		= fields.DecimalField('')
	s10chargeDeliv	= fields.DecimalField('')
	s10chargeReq	= fields.DecimalField('')
	s19chargeDeliv	= fields.DecimalField('')
	s19chargeReq	= fields.DecimalField('')
	s20chargeDeliv	= fields.DecimalField('')
	s20chargeReq	= fields.DecimalField('')
	scavchargeDeliv	= fields.DecimalField('')
	scavchargeReq	= fields.DecimalField('')
	
	s2emitDeliv		= fields.DecimalField('')
	s2emitReq		= fields.DecimalField('')
	s4emitDeliv		= fields.DecimalField('')
	s4emitReq		= fields.DecimalField('')
	s11emitDeliv	= fields.DecimalField('')
	s11emitReq		= fields.DecimalField('')
	s18emitDeliv	= fields.DecimalField('')
	s18emitReq		= fields.DecimalField('')
	s20emitDeliv	= fields.DecimalField('')
	s20emitReq		= fields.DecimalField('')
	'''

	# This is like a weird __init__ since I couldn't get __init__ to work properly
	def setForm(self):
		self.setUserChoices()

	def setUserChoices(self):
		choices = [('', 'Please Select')] # Empty string means that required validator returns false
		users = models.User.query.order_by('name asc').all()
		for u in users:
			choices.append((str(u.id), u)) # Two parenthesis since the choice pairs are tuples
		self.user.choices = choices

	def read_report(self, report):
		self.user.data 					= str(report.user) # Must use string for form.
		self.personnel.data				= report.personnel
		self.postTime.data				= report.postTime
		self.shiftStart.data			= report.shiftStart
		self.shiftEnd.data				= report.shiftEnd
		self.goals.data					= report.goals
		self.progress.data				= report.progress
		self.problems.data				= report.problems
		self.nextShift.data				= report.nextShift
		self.briefSummary.data			= report.briefSummary
		self.other.data					= report.other
		self.usefulBeam.data			= report.usefulBeam
		self.unschedAccDown.data		= report.unschedAccDown
		self.unschedUserDown.data		= report.unschedUserDown
		self.physAvail.data				= report.physAvail
		self.requested_time.data = report.requested_time