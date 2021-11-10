from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from functools import wraps
import jwt
from sqlalchemy.orm import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSECRETSECRETKEY'
app.debug = True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Please input token'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated



@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This route has restricted permission only for users with token.'})



class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String())
    password = db.Column(db.String())
    token = db.Column(db.String())

    def __init__(self, login, password, token):
        self.login = login
        self.password = password
        self.token = token
    def __repr__(self):
        return f"< {self.login}>"

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session.query(User) \
            .filter(User.id == auth.username,) \
            .update({User.token: token})

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
