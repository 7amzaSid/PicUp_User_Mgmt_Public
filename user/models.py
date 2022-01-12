from flask_login import UserMixin

class User(UserMixin):
    username = str
    password = str
    user_list = []

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_authenticated = False

    @property
    def is_authenticated(self):
        return self._is_authenticated
    
    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    def queue(user):
        print(User.user_list)
        User.user_list.append(user)
    
    def dequeue(user):
        print(User.user_list)
        User.user_list.remove(user)
    
    def get(user_id):
        for user in User.user_list:
            if user.username == user_id: 
                return user
        return None

    def get_id(self):
        return self.username
