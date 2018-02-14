from flask import Flask, render_template, url_for, redirect, request, session, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm
from app.models import User
from app.forms import RegisterForm, LoginForm

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        db.session.add(g.user)
        db.session.commit()
        
@lm.user_loader
def load_user(id):
	return User.query.get(id)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
	if g.user.is_authenticated:
		return redirect(url_for('home', username=g.user))
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = User.query.filter_by(username=request.form["username"], password=request.form["password"]).first()
		if user is None:
			return redirect(url_for('index'))
		if login_user(user):
			return redirect(url_for('home', username=g.user))
	return render_template("index.html", form=form, title="Login")

@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm(request.form)
	if request.method == "POST" and form.validate_on_submit():
		username = request.form["username"]
		password = request.form["password"]
		masukan = User(username=username, password=password)
		db.session.add(masukan)
		db.session.commit()
		return redirect(url_for('success'))
	return render_template("register.html", form=form, title="Register")

@app.route("/success")
def success():
	return render_template("success.html", title="Success")

@app.route("/home/<username>")
@login_required
def home(username):
	users = User.query.filter_by(username=username).first()
	return render_template("home.html", username=username, users=users, title="Home")

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
