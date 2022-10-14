from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from facebook_api import compare_all
import os

load_dotenv()
db_pass = os.getenv("password")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@localhost/ridedirt'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class TrailSystem(db.Model):

	id_ = db.Column(db.Integer, primary_key=True)
	front_name = db.Column(db.String(100))
	fb_name = db.Column(db.String(100))
	fb_id = db.Column(db.String(100))
	fb_url = db.Column(db.String(100))
	location = db.Column(db.String(100))
	status = db.Column(db.String(100))
	updated = db.Column(db.DateTime)


	def __init__(self, front_name, fb_name, fb_id, fb_url, location, status, updated):

		self.front_name = front_name
		self.fb_name = fb_name
		self.fb_id = fb_id
		self.fb_url = fb_url
		self.location = location
		self.status = status
		self.updated = updated


	def update_fb_picture_status():

		db_list = compare_all()
		for row in db_list:
			data = TrailSystem(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
			db.session.add(data)
		db.session.commit()


if __name__ == "__main__":

	db.create_all()
	TrailSystem.update_fb_picture_status()


	


