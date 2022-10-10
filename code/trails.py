from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from facebook_api import get_static, compare_all
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
	open_ = db.Column(db.String(100))
	closed = db.Column(db.String(100))


	def __init__(self, front_name, fb_name, fb_id, fb_url, location, open_, closed):

		self.front_name = front_name
		self.fb_name = fb_name
		self.fb_id = fb_id
		self.fb_url = fb_url
		self.location = location
		self.open_ = open_
		self.closed = closed


	def create_trail_columns():

		row_list = get_static()
		for row in row_list:
			print(row)
			data = TrailSystem(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
			db.session.add(data)
		db.session.commit()

	def update_binary_status():

		status_dict = compare_all()
		for name, status in status_dict.items():
			if status == 'open':
				found_name = TrailSystem.query.filter_by(fb_name=name).first()
				found_name.open_ = "Everything's Open!" 
				found_name.closed= ""
				db.session.commit()
			else:
				found_name = TrailSystem.query.filter_by(fb_name=name).first()
				found_name.open_ = "" 
				found_name.closed= "Trails are too muddy."
				db.session.commit()



def main(*args):
	
	for arg in args:
		if arg == 'create_static':
			TrailSystem.create_trail_columns()
		if arg == 'check_status':
			TrailSystem.update_binary_status()

if __name__ == "__main__":

	db.create_all()

	main('create_static', 'check_status')


	


