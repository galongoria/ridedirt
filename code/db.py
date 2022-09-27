from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from facebook_api import get_static
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
	location = db.Column(db.String(100))
	status = db.Column(db.String(100))

	def __init__(self, name, location, status):

		self.front_name = front_name
		self.fb_name = fb_name
		self.fb_id = fb_id
		self.location = location
		self.status = status


def insert_static_trail_data():

	data = get_static()

	print(data)






if __name__ == "__main__":

	db.create_all()

	insert_static_trail_data()

	


