from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from app import models


class LoginForm(Form):
	user 			= fields.SelectField('User Group', choices=[('error', 'FAILED TO LOAD USER GROUPS')], validators=[Required()], default=0)
	shifts			= fields.SelectField('Shift', choices=[('error', 'FAILED TO LOAD USER GROUPS')], validators=[Required()], default=0)
	personnel		= fields.TextAreaField('Shift Leader/Shift Personnel')
	
	goals			= fields.TextAreaField('Goals')
	progress		= fields.TextAreaField('Progress')
	problems		= fields.TextAreaField('Problems')
	nextShift		= fields.TextAreaField('To Do On Next Shift')
	briefSummary	= fields.TextAreaField('Brief Summary', validators = [Required()])
	other			= fields.TextAreaField('Other')
	
	usefulBeam		= fields.IntegerField('Useful Beam Time')
	unschedAccDown	= fields.IntegerField('Unscheduled Accelerator Downtime')
	unschedUserDown	= fields.IntegerField('Unscheduled User Downtime')
	physAvail		= fields.IntegerField('AcceleratorPhysicistAvailability')
	
	def setForm(self):
		self.setUserChoices()
		self.setShiftChoices()
	
	def setUserChoices(self):
		choices = [('', 'Please Select')] # Empty string means that required validator returns false
		users = models.User.query.all()
		for u in users:
			choices.append((str(u.id), u.name))
		self.user.choices = choices
	
	def setShiftChoices(self):
		self.shifts.choices = [('', 'Please Select'), ('Day', 'Day'), ('Swing', 'Swing'), ('Owl', 'Owl')]