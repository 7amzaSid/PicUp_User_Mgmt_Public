from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

app = Flask(__name__)

@app.route('/')
def home():
    return "Home route"

app.config["SECRET_KEY"] = "guessable key"
DB_URI = "mongodb+srv://hamza:123@cluster0.oyduo.mongodb.net/user_management?retryWrites=true&w=majority"

login_manager = LoginManager(app)
db = MongoEngine(app)
db.connect(host=DB_URI)

from . import auth
