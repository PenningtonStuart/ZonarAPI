from user import User

users = [
    User(1, 'Stuart', 'Pennington', 'stuart.lee.pennington@gmail.com', 'thisHash')
]

username_mapping = {u.email: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(email, password):
    user = username_mapping.get(email, None)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
