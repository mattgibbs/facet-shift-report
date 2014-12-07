from flask import render_template, flash, redirect, url_for, request
from app import app, db, models
from forms import LoginForm, UserForm
import datetime

@app.errorhandler(404)
def internalerror(error):
	return render_template('404.html'), 404

@app.route('/')
def root_index():
	return redirect('index')

@app.route('/index')
@app.route('/index/<int:userid>')
@app.route('/index/<username>/')
def index(userid = None, username = None):
	user = None
	if userid:
		user = db.session.query(models.User).get(userid)
		if user:
			reports = user.reports.order_by('id desc')
		else:
			flash('Invalid user group')
			return redirect('index')
	elif username or request.args.get('userGroup',''):
		if username:
			userToFind = username
		elif request.args.get('userGroup',''):
			userToFind = request.args.get('userGroup','')
		
		user = db.session.query(models.User).filter(models.User.name == userToFind).all()
		if user:
			return redirect("index/" + str(user[0].id))# all() returns a list, but it only has one user group in there.
		else:
			flash(username + ' is an invalid user group')
			return redirect('index')
	else:
		reports = db.session.query(models.ShiftReport).order_by('id desc').all()#models.ShiftReport.query.order_by('id desc').all()
	for r in reports:
		print r.id, r.shiftStart, r.user
	return render_template("index.html", reports=reports, user=user)


@app.route('/shift_summary_form/', methods=['GET', 'POST'])
@app.route('/shift_summary_form/<int:reportid>', methods=['GET', 'POST'])
def shift_summary_form(reportid = None):
	form = LoginForm()
	form.setForm()
	if form.validate_on_submit():
		try:
			if reportid:
				report = models.ShiftReport.query.get(reportid)
				report.read_form(form)
			else:
				report = models.ShiftReport(form)
				db.session.add(report)
			db.session.commit()
			dbmessage = "Successfully uploaded to database, "
			try:
				report.post_to_logbook()
				logmessage = "and FACET E-Log entry created."
			except HTTPError:
				logmessage = "but could not create FACET entry."
			flash(dbmessage + logmessage)
		except:
			flash("Error uploading to database.")
		return redirect('index')
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			# Fill out form with data from database
			print report.user
			form.read_report(report)
			print form.user.data
		else:
			# Report ID does not exist
			flash("Report does not exist")
			return redirect('shift_summary_form/')
	return render_template('shift_report.html', form=form)

@app.route('/view_report')
@app.route('/view_report/')
@app.route('/view_report/<int:reportid>')
def view_report(reportid = None):
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			return render_template('view_report.html', report=report)
		else:
			flash("Failed to load report #" + str(reportid) + ". Report does not exist.")
			return redirect('index')
	flash("No report specified. Redirected to root.")
	return redirect('index')

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
	form = UserForm()
	if form.validate_on_submit():
		try:
			# TODO check that user doesn't already exist
			user = models.User(form)
			db.session.add(user)
			db.session.commit()
			flash("Successfully created user " + form.data['userName'])
		except:
			flash("Error creating user. Exception " + type(e))
		
		return redirect('index')
	return render_template('create_user.html', form=form)