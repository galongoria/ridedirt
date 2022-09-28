from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from facebook_api import get_static
from trails import Trail
import os

load_dotenv()
db_pass = os.getenv("password")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@localhost/ridedirt'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

db = SQLAlchemy(app)




