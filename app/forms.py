from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	textbox = TextAreaField('Box', validators = [Required()])