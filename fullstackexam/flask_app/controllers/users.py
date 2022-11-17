from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/register', methods=["POST"])
def register():
    valid_user = User.create_valid_user(request.form)
    if not valid_user:
        return redirect('/')
    session['user_id'] = valid_user.id
    return redirect('/reports/dashboard')

@app.route('/login', methods=["POST"])
def login():
    valid_user = User.login_verification(request.form)
    if not valid_user:
        return redirect('/')
    
    session["user_id"] = valid_user.id
    print(f"printing user_id {valid_user.id}")
    return redirect('/reports/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
