from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from facebook_api import get_static, compare_all
import os

load_dotenv()
db_pass = os.getenv("password")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@localhost/ridedirt'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

db = SQLAlchemy(app)

class Trail(db.Model):

	id_ = db.Column(db.Integer, primary_key=True)
	front_name = db.Column(db.String(100))
	fb_name = db.Column(db.String(100))
	fb_id = db.Column(db.String(100))
	fb_url = db.Column(db.String(100))
	location = db.Column(db.String(100))
	status = db.Column(db.String(100))

	def __init__(self, front_name, fb_name, fb_id, fb_url, location, status):

		self.front_name = front_name
		self.fb_name = fb_name
		self.fb_id = fb_id
		self.fb_url = fb_url
		self.location = location
		self.status = status

	def insert_static_trail_data():

		row_list = get_static()
		for row in row_list:
			print(row)
			data = Trail(row[0], row[1], row[2], row[3], row[4], row[5])
			db.session.add(data)
		db.session.commit()

	def insert_trail_status():

		status_dict = compare_all()
		for name, status in status_dict.items():
			found_name = Trail.query.filter_by(fb_name=name).first()
			found_name.status = status
			db.session.commit()


	def main(*args):
		
		for arg in args:
			if arg == 'update_static':
				Trail.insert_static_trail_data()
			if arg == 'check_status':
				Trail.insert_trail_status()


	


