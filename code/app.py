from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
password=os.getenv("password")

app=Flask(__name__)
app.config("SQLALCHEMY_DATABASE_URI")='postgresql:///postgres:password@localhost/ridedirt'
db=SQLAlchemy(app)

@app.route('/')
def hello():
	return "Hello World"




if __name__ == "__main__":

	app.run(debug=True)