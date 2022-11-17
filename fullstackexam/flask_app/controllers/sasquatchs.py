from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.sasquatch import Sasquatch
from flask_app.models.user import User

@app.route("/reports/dashboard")
def reports():
    if "user_id" not in session:
        flash("You must log in to access to the dashboard")
        return redirect('/')

    user = User.get_by_id(session['user_id'])
    reports = Sasquatch.get_all()
    print(f"This is Printing   {reports}")
    return render_template("dashboard.html", user = user , reports = reports)

@app.route('/reports/<int:report_id>')
def report_detail(report_id):
    user = User.get_by_id(session["user_id"])
    report = Sasquatch.get_by_id(report_id)
    
    return render_template("report_detail.html", user = user, report = report)

@app.route('/reports/create')
def report_create_page():
    if "user_id" not in session:
        flash("You must log in to access to the dashboard")
        return redirect('/')
    user = User.get_by_id(session['user_id'])

    return render_template("create_report.html", user = user)

@app.route('/reports/edit/<int:report_id>')
def report_edit_page(report_id):
    user = User.get_by_id(session["user_id"])
    report = Sasquatch.get_by_id(report_id)
    return render_template('edit_report.html', report = report, user = user)

@app.route('/reports', methods=["POST"])
def create_report():
    if "user_id" not in session:
        flash("You must log in to access to the dashboard")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    data = {
        "location" : request.form['location'],
        "description" : request.form['description'],
        "siting_date" : request.form['siting_date'],
        "sasquatch" : request.form['sasquatch'],
        "user_id" : session['user_id']
    }
    valid_report = Sasquatch.create_valid_report(data)

    if valid_report:
        return redirect(f'/reports/edit/{valid_report.id}')
    return redirect('/reports/create')

@app.route('/reports/<int:report_id>' , methods=['POST'])
def update_report(report_id):
    valid_report = Sasquatch.update_report(request.form, session['user_id'])

    if not valid_report:
        return redirect(f'/reports/edit/{report_id}')

    return redirect(f"/reports/{report_id}")

@app.route("/reports/delete/<int:report_id>")
def delete_by_id(report_id):
    Sasquatch.delete_report_by_id(report_id)
    return redirect("/reports/dashboard")