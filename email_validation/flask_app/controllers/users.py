from flask_app.models.user import User
from flask_app import app
from flask import render_template, request, redirect

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def users():
    return render_template('showuser.html', users = User.get_all())
@app.route('/create', methods=["POST"])
def create_user():

    if not User.validate_user(request.form):
        return redirect('/')
    User.save(request.form)
    return redirect('/dashboard')