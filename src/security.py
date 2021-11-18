from user import User


def authenticate(email, password):
    user = User.find_by_username(email)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id, None)
