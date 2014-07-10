from flask.ext.wtf import Form
from wtforms import SelectField, TextField, BooleanField, TextAreaField
from wtforms.validators import Required

class LoginForm(Form):
	user 		= SelectField('User Group')
	openid 		= TextField('openid', validators = [Required()])
	goals 		= TextAreaField('Goals', validators = [Required()])