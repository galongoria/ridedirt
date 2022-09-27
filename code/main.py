from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from pictures import get_all
import os

app=Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("secret_key")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'trails.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class trails(db.Model):

	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	location = db.Column("locaiton", db.String(100))
	status = db.Column("status", db.String(100))

	def __init__(self, name, email):
		self.name = name
		self.location = location

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/")
def trails():

	status_dict = get_all()
	for name, status in status_dict.items():
		

@app.route("/view")
def view():
	return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method=="POST":
		session.permanent = True
		user = request.form["nm"]
		session["user"] = user
		found_user = users.query.filter_by(name=user).first()
		if found_user:
			session["email"] = found_user.email
		else:
			usr = users(user, "")
			db.session.add(usr)
			db.session.commit()
		flash(f"Login Successful!")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash(f"Already Loggied In!")
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
	email=None
	if "user" in session:
		user = session["user"]
		if request.method == "POST":
			email = request.form["email"]
			session["email"] = email
			found_user = users.query.filter_by(name=user).first()
			found_user.email = email
			db.session.commit()
			flash("Email was saved!")
		else:
			if "email" in session:
				email = session["email"]
		return render_template("user.html", email=email)
	else:
		flash(f"You are not logged in!")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	flash(f"You have been logged out!", "info")
	session.pop("user", None)
	session.pop("email", None)
	return redirect(url_for("login"))


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)