from flask import Flask, jsonify
from flask_login import LoginManager, current_user
import pymongo

# our Flask app
app = Flask(__name__)

# setting up PyMongo, db is database used
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.oyduo.mongodb.net/user_management?retryWrites=true&w=majority")
db = client.user_database

app.config["SECRET_KEY"] = "<secret key>"

# login manager for managing login sessions 
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = enter a view here so app doesn't freeze when accessing login_req routes

from user import user_mgmt_routes

@app.route('/')
def home():
    '''
    Home route that displays all users currently saved in database, 
    as well as the logged in user if there is one
    '''
    res = {
        'page': 'home',
        'users': [],
        'current_user': None
    }
    if current_user.is_authenticated:
        res['current_user'] = current_user.username + ", authenticated"
    for user in db.users.find():
        res['users'].append(str(user))
    return jsonify(res)

@app.route("/drop")
def drop():
    db.users.drop()
    if len(list(db.users.find())) == 0:
        return jsonify("table dropped")
    else:
        return jsonify("error dropping table")
