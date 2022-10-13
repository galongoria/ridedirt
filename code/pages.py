from flask import Flask, redirect, url_for, render_template, session, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from trails import TrailSystem
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


@app.route("/logout")
def logout():
	flash("You have been logged out!", "info")
	session.pop("user", None)
	session.pop("email", None)
	return redirect(url_for("login"))


if __name__ == "__main__":

	db.create_all()
	app.run(debug=True)