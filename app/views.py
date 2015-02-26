from flask import render_template, flash, redirect, url_for, request
from app import app, db, models
from forms import ShiftForm, UserForm
from datetime import datetime
import nl2br
import datetimeformat
from requests import HTTPError
from requests import ConnectionError

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
		if user == None:
			flash('Invalid experiment ID.')
			return redirect('index')
	elif username or request.args.get('userGroup',''):
		if username:
			userToFind = username
		elif request.args.get('userGroup',''):
			userToFind = request.args.get('userGroup','')
		user = db.session.query(models.User).filter(models.User.name == userToFind).first()
		if user == None:
			flash((username or request.args.get('userGroup','')) + ' is an invalid experiment name.')
			return redirect('index')			
	
  #If there is a user specified, get their reports, otherwise, just get all reports.
	reports = None
	if user:
		reports = db.session.query(models.ShiftReport).filter(models.ShiftReport.user == user.id)
	else:
		reports = db.session.query(models.ShiftReport)
	
  #If there is a start and end date specified, only get reports between those dates.
	start_date = None
	end_date = None
	start_date_str = request.args.get('start_date')
	end_date_str = request.args.get('end_date')
	if start_date_str and end_date_str:
		try:
			start_date = datetime.strptime(request.args.get('start_date'),"%Y-%m-%d")
		except ValueError:
			flash('Could not parse start date, ignoring date filter.')
		try:
			end_date = datetime.strptime(request.args.get('end_date'),"%Y-%m-%d")
		except ValueError:
			flash('Could not parse end date, ignoring date filter.')
		if start_date and end_date:
			reports = reports.filter(models.ShiftReport.shiftEnd.between(start_date, end_date))

	#Unless the user requests seeing everything, don't include hidden reports.
	if (request.args.get('show_hidden') == None) or (request.args.get('show_hidden').lower() != "true"):
		hidden_reports = reports.filter(models.ShiftReport.hidden == True)
		reports = reports.except_(hidden_reports)
	
	#Always order the reports by id
	reports = reports.order_by('shift_report_id desc')
	
	return render_template("index.html", reports=reports, user=user, start_date=start_date_str, end_date=end_date_str)
	
@app.route('/shift_summary_form/', methods=['GET', 'POST'])
@app.route('/shift_summary_form/<int:reportid>', methods=['GET', 'POST'])
def shift_summary_form(reportid = None):
	form = ShiftForm()
	form.setForm()
	if form.validate_on_submit():
		if reportid:
			report = models.ShiftReport.query.get(reportid)
			report.read_form(form)
		else:
			report = models.ShiftReport(form)
			db.session.add(report)
			
		try:
			db.session.commit()
			dbmessage = "Successfully uploaded to database, "
		except:
			flash("Could not create shift report.")
			return redirect('index')
			
		try:
			success = report.post_to_logbook()
			if success:
				logmessage = "and FACET E-Log entry created."
			else:
				logmessage = "but could not create FACET entry."
		except (HTTPError, ConnectionError):
			logmessage = "but could not create FACET entry."
		
		flash(dbmessage + logmessage)
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

@app.route('/create_experiment/', methods=['GET', 'POST'])
def create_experiment():
	form = UserForm()
	if form.validate_on_submit():
		try:
			# TODO check that user doesn't already exist
			user = models.User(form)
			db.session.add(user)
			db.session.commit()
			flash("Successfully created experiment " + form.data['userName'])
		except:
			flash("Error creating experiment. Exception " + type(e))
		
		return redirect('experiments')
	return render_template('create_experiment.html', form=form)
	
@app.route('/edit_experiment/<int:userid>', methods=['GET', 'POST'])
def edit_experiment(userid = None):
	form = UserForm()
	try:
		user = models.User.query.get(userid)
	except:
		flash("Error fetching experiment.  Exception " + type(e))
		
	if form.validate_on_submit():
		try:
			# TODO check that user doesn't already exist
			print form.userName.data
			user.read_form(form)
			print user.name
			db.session.commit()
			flash("Successfully updated experiment " + form.data['userName'])
		except:
			flash("Error editing experiment.")
		return redirect('index')
	else:
		form.read_user(user)
		
	return render_template('edit_experiment.html', form=form, user=user)
	
@app.route('/experiments')
@app.route('/experiments/')
def list_experiments():
	users = db.session.query(models.User).order_by('name asc').all()
	return render_template('list_experiments.html', users=users)
	