from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from login_helper import login_user, logout_user, login_decorator
from util import uuid_32


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@127.0.0.1:5432/session_user_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    # id
    id = db.Column(db.String(32), primary_key=True, default=uuid_32)
    # 用户账号
    username = db.Column(db.String(20), index=True)
    # 密码
    password = db.Column(db.String(20))
    # 被删除
    is_deleted = db.Column(db.Boolean, default=False)


@app.route('/registered', methods=['POST'])
def registered():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User(username=username,
                password=password)
    db.session.add(user)
    db.session.commit()
    return 'ok'


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username==username).first()
    if user is None:
        return 'error', 403
    if user.password != password:
        return 'error', 403
    login_user(user.id)
    return 'ok'


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return 'ok'


@app.route('/test_login')
@login_decorator
def test_login():
    print(11111111111)
    return 'ok'


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, host='0.0.0.0')


