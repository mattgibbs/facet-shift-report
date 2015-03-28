from flask import render_template, flash, redirect, url_for, request, Response
from functools import wraps
from app import app, db, models
from forms import ShiftForm, UserForm
from datetime import datetime
import nl2br
import datetimeformat
import secrets
import os.path
from requests import HTTPError
from requests import ConnectionError

@app.errorhandler(404)
def internalerror(error):
	return render_template('404.html'), 404

@app.route('/')
def root_index():
	return redirect('index')

@app.route('/index')
@app.route('/index/')
@app.route('/index/<int:userid>')
@app.route('/index/<username>/')
def index(userid = None, username = None, admin=False):
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
	if ((request.args.get('show_hidden') == None) or (request.args.get('show_hidden').lower() != "true")) and not admin:
		hidden_reports = reports.filter(models.ShiftReport.hidden == True)
		reports = reports.except_(hidden_reports)
	
	#Always order the reports by end date
	reports = reports.order_by('shift_report_shiftEnd desc')
	
	#Determine if this is a CSV request.  If so, we'll return CSV for the report.
	path, extension = os.path.splitext(request.base_url)
	print(request.base_url)
	if extension == ".csv":
		reports = reports.filter(models.ShiftReport.submitted == True)
		return Response(generate_csv_for_reports(reports), mimetype='text/csv')
	return render_template("index.html", reports=reports, user=user, start_date=start_date_str, end_date=end_date_str, admin=admin)

@app.route('/index.csv')
@app.route('/index/<int:userid>.csv')
@app.route('/index/<username>.csv')
def csv_index(userid = None, username = None):
	return index(userid, username)


@app.route('/summaries/', methods=['GET'])
def summaries():
  #If there is a start and end date specified, only get reports between those dates.
	start_date = None
	end_date = None
	start_date_str = request.args.get('start_date')
	end_date_str = request.args.get('end_date')
	reports = db.session.query(models.ShiftReport)
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
	if ((request.args.get('show_hidden') == None) or (request.args.get('show_hidden').lower() != "true")):
		hidden_reports = reports.filter(models.ShiftReport.hidden == True)
		reports = reports.except_(hidden_reports)
	
	if request.args.get('show_unsubmitted') == None or not (request.args.get('show_unsubmitted').lower() == "true"):
		reports = reports.filter(models.ShiftReport.submitted == True)
	
	#Always order the reports by id
	reports = reports.order_by('shift_report_shiftEnd desc')
	
	return render_template("summaries.html", reports=reports, start_date=start_date_str, end_date=end_date_str)

@app.route('/summaries/raw/', methods=['GET'])
def raw_summaries():
  #If there is a start and end date specified, only get reports between those dates.
	start_date = None
	end_date = None
	start_date_str = request.args.get('start_date')
	end_date_str = request.args.get('end_date')
	reports = db.session.query(models.ShiftReport)
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
	if ((request.args.get('show_hidden') == None) or (request.args.get('show_hidden').lower() != "true")):
		hidden_reports = reports.filter(models.ShiftReport.hidden == True)
		reports = reports.except_(hidden_reports)
	
	#Always order the reports by id
	reports = reports.order_by('shift_report_shiftEnd desc')
	return render_template("raw_summaries.html", reports=reports, start_date = start_date_str, end_date = end_date_str)
		


@app.route('/shift_summary_form/', methods=['GET'])
@app.route('/shift_summary_form/<int:reportid>', methods=['GET'])
def shift_summary_form(reportid = None):
	form = ShiftForm()
	form.setForm()
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			# Fill out form with data from database
			form.read_report(report)
			form.validate()
		else:
			# Report ID does not exist
			flash("Report does not exist")
			return redirect(url_for('shift_summary_form'))
	return render_template('shift_report.html', form=form, reportid=reportid)

@app.route('/save_shift_form/', methods=['POST'])
@app.route('/save_shift_form/<int:reportid>', methods=['POST'])
def save_shift_form(reportid = None):
	form = ShiftForm()
	form.setForm()
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		report.read_form(form)
	else:
		report = models.ShiftReport(form)
		db.session.add(report)
	
	try:
		db.session.commit()
		flash("Shift report saved.")
		return redirect(url_for('shift_summary_form', reportid = report.id))
	except: 
		flash("Could not save shift report.")
		return render_template('shift_report.html', form=form)

@app.route('/submit_shift_form/', methods=['POST'])
@app.route('/submit_shift_form/<int:reportid>', methods=['POST'])
def submit_shift_form(reportid = None):
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
			flash("Could not submit shift report.")
			if reportid:
				return redirect(url_for('shift_summary_form', reportid=reportid))
			else:
				return render_template('shift_report.html', form=form, reportid=None)
			
		try:
			new_entry_url = report.post_to_logbook()
			if new_entry_url:
				report.logbook_entry_url = new_entry_url
				report.submitted = True
				db.session.commit()
				logmessage = "and FACET E-Log entry created."
			else:
				logmessage = "but could not create FACET entry."
		except (HTTPError, ConnectionError):
			logmessage = "but could not create FACET entry."
		flash(dbmessage + logmessage)
		return redirect('index')
		
	flash("Could not submit shift report, please check the form for errors.")
	if reportid:
		return redirect(url_for('shift_summary_form', reportid=reportid))
	else:
		return render_template('shift_report.html', form=form, reportid=None)

@app.route('/view_report')
@app.route('/view_report/')
@app.route('/view_report/<int:reportid>')
def view_report(reportid = None, admin=False):
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			return render_template('view_report.html', report=report, admin=admin)
		else:
			flash("Failed to load report #" + str(reportid) + ". Report does not exist.")
			return redirect('index')
	flash("No report specified. Redirected to root.")
	return redirect('index')
		
@app.route('/experiments')
@app.route('/experiments/')
def list_experiments():
	users = db.session.query(models.User).order_by('name asc').all()
	return render_template('list_experiments.html', users=users)
	
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == secrets.admin_username and password == secrets.admin_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
		
@app.route('/create_experiment/', methods=['GET', 'POST'])
@requires_auth
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
@requires_auth
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
		return redirect(url_for('list_experiments'))
	else:
		form.read_user(user)
		
	return render_template('edit_experiment.html', form=form, user=user)

@app.route('/admin/index')
@app.route('/admin/index/')
@app.route('/admin/index/<int:userid>')
@app.route('/admin/index/<username>/')
@requires_auth
def admin_index(userid = None, username = None):
	return index(userid = userid, username = username, admin=True)
	
@app.route('/admin/view_report/<int:reportid>')
@requires_auth
def admin_view_report(reportid = None):
	return view_report(reportid = reportid, admin=True)

@app.route('/admin/toggle_report_hidden/<int:reportid>')
@requires_auth
def admin_toggle_report_hidden(reportid = None):
	if reportid:
		report = db.session.query(models.ShiftReport).get(reportid)
		if report:
			#Hide or show the report
			if report.hidden:
				report.hidden = False
			else:
				report.hidden = True
			db.session.commit()
			flash("Report hidden." if report.hidden else "Report shown.")
			if request.args.get('next') == 'index':
				return redirect(url_for('admin_index'))
			elif request.args.get('next'):
				userid = int(request.args.get('next'))
				return redirect(url_for('admin_index', userid=userid))
			return redirect(url_for('admin_view_report', reportid = report.id))
		else:
			abort(404)
	flash("No report specified. Redirected to admin page.")
	return redirect(url_for('admin_index'))

@app.route('/admin/delete_report/<int:reportid>')
@requires_auth
def admin_delete_report(reportid = None):
	if reportid:
		report = db.session.query(models.ShiftReport).get(reportid)
		if report:
			#Delete the report
			db.session.delete(report)
			db.session.commit()
			flash("Report deleted.")
			if request.args.get('next') == 'index':
				return redirect(url_for('admin_index'))
			elif request.args.get('next'):
				userid = int(request.args.get('next'))
				return redirect(url_for('admin_index', userid=userid))
			return redirect(url_for('admin_index'))
		else:
			abort(404)
	flash("No report specified. Redirected to admin page.")
	return redirect(url_for('admin_index'))
	
	
def generate_csv_for_reports(reports):
	output_rows = ['Totals',','.join(['Experiment', 'Hours Delivered', 'Hours Requested', 'Hours Accelerator Down', 'Hours User Off', 'Hours Total'])]
	totals = {}
	for report in reports:
		if not (str(report.author) in totals):
			totals[str(report.author)] = {'Hours Delivered': 0, 'Hours Requested': 0, 'Hours Accelerator Down': 0, 'Hours User Off': 0, 'Hours Total': 0}
		totals[str(report.author)]['Hours Delivered'] += report.usefulBeam
		totals[str(report.author)]['Hours Requested'] += report.requested_time
		totals[str(report.author)]['Hours Accelerator Down'] += report.unschedAccDown
		totals[str(report.author)]['Hours User Off'] += report.unschedUserDown
		totals[str(report.author)]['Hours Total'] += report.totalHours()
	
	for report_title, report_totals in totals.iteritems():
		output_rows.append(','.join([report_title, str(report_totals['Hours Delivered']), str(report_totals['Hours Requested']), str(report_totals['Hours Accelerator Down']), str(report_totals['Hours User Off']), str(report_totals['Hours Total'])]))
	
	output_rows.extend(['', 'Shift by shift', ','.join(['Experiment', 'Hours Delivered', 'Hours Requested', 'Hours Accelerator Down', 'Hours User Off', 'Hours Total'])])
	for report in reports:
		output_rows.append(','.join([str(report.author), str(report.usefulBeam), str(report.requested_time), str(report.unschedAccDown), str(report.unschedUserDown), str(report.totalHours())]))
	
	return '\n'.join(output_rows)