from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from trails import TrailSystem
from facebook_api import compare_all
from itertools import zip_longest
import os


### dotenv secrets ###

load_dotenv()
db_pass = os.getenv("password")
secret_key = os.getenv("secret_key")


### App config and database setup###

app=Flask(__name__)
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@localhost/ridedirt'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.jinja_env.filters['zip_longest'] = zip_longest

db = SQLAlchemy(app)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/trails", methods=["GET"])
def trails():

	return render_template('trails.html', values=TrailSystem.query.all(), zip_longest=zip_longest)


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