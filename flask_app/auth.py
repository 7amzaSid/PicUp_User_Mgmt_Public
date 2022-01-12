from flask import Blueprint
from flask_app.models import User
from . import app, db

# View functions
@app.route('/register')
def register():
    user = User()
    user.username = "Hamza"
    user.password = "some password"
    user.save()
    return user.get_id()

@app.route('/login')
def login():
    return "login at this route"

@app.route('/logout')
def logout():
    return "logout at this route"