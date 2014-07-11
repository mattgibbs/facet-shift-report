from flask import render_template, flash, redirect
from app import app, db, models
from forms import LoginForm

@app.route('/')
def index():
	posts = [
		{
			'author': {'nickname': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'nickname': 'Sarah'},
			'body': 'The Avengers movie was so cool!'
		},
		]
	return render_template("index.html", posts=posts)


@app.route('/shift_summary_form/', methods=['GET', 'POST'])
def shift_summary_form():
	choices = []
	users = models.User.query.all()
	for u in users:
		choices.append((str(u.id), u.name))
	form = LoginForm()
	form.setChoices(choices)
	if form.validate_on_submit():
		flash("WHATUP")
		return redirect('/')
	return render_template('shift_report.html', form=form)