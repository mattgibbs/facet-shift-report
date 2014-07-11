from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required

class Body(Form):
	goals		= fields.TextAreaField('Goals', validators = [Required()])
	progress	= fields.TextAreaField('Progress', validators = [Required()])

class LoginForm(Form):
	user 		= fields.SelectField('User Group', choices=[('error', 'FAILED TO LOAD USER GROUPS')])
	textboxes 	= fields.FieldList(fields.TextAreaField('Name', validators = [Required()]), min_entries=1)
	body		= fields.FormField(Body)
	
	def setChoices(self, inputChoices):
		self.user.choices = inputChoices