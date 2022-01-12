from flask import Flask, url_for, redirect, jsonify
from app import app, db
from user.models import User
from app import login_manager
from flask_login import current_user, login_user, login_required, logout_user

@login_manager.user_loader
def load_user(user_id):
    '''
    Used by LoginManager to retrieve the user object that is logged in for this session
    '''
    return User.get(user_id)

@app.route('/user/signup/<credentials>')
def singup(credentials):
    '''
    Parses colon delimeted credentials from URL of the format 'username:password'
    If username and password are valid, create User object
    - Store document in db containing username and password
    - queue User object so LoginManager can retrieve its reference via User.get(username) 
    '''
    credentials = credentials.split(":")
    
    if len(credentials) != 2:
        return jsonify("username or password missing, you must enter both a username and password")

    username = credentials[0]
    password = credentials[1]
    
    user = User(username=username, password=password)

    users_with_username = list(db.users.find({"username": username}))
    
    if len(username) > 0 and len(password) > 0 and len(users_with_username) == 0:
        db.users.insert_one({
            "username": user.username,
            "password": user.password
        })
        return jsonify("signup success")

    elif len(users_with_username) > 0: 
        return jsonify("username taken")
    
    else:
         return jsonify("signup failure")

@app.route("/user/login/<credentials>")
def login(credentials):
    '''
    Parses colon delimeted credentials of format 'username:password'
    if username and password match that of a document stored in db, 
    - login user using flask_login function login_user(user)
    - queue User object so its reference can be retrieved by LoginManager via User.get(username)
    '''
    credentials = credentials.split(":")
    
    if len(credentials) != 2:
        return jsonify("must enter username and password")
    
    username = credentials[0]
    password = credentials[1]

    user_list = db.users.find({
        "username": username,
        "password": password
    })
    user_list = list(user_list)

    if len(user_list) > 0:
        user = User(username=username, password=password)
        User.queue(user)
        
        login_user(user)
        
        user.is_authenticated = True

        return jsonify(current_user.username + " has been logged in")
    
    return jsonify("invalid credentials")

@app.route("/user/logout")
@login_required
def logout():
    '''
    logs out current_user only if they are logged in (same as saying only if current_user.is_auth)
    dequeue current_user as they are no longer needed for retrieval by LoginManager
    '''
    User.dequeue(current_user)
    logout_user()
    return redirect(url_for("home"))

@app.route("/user/cur_user")
def cur_user():
    '''
    returns json of current user username and password if they are authenticated
    '''
    res = {}
    if current_user.is_authenticated:
        res["username"] = current_user.username
        res["password"] = current_user.password
    return jsonify(res)



    