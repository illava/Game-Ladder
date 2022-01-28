from flask import Flask, request, abort, redirect, Response, url_for, render_template
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(128)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self.password = password
        self.value = 0
        return

    def is_activate(self):
        return True

    def get_id(self):
        return self.id


class UsersRepository:
    def __init__(self):
        self.users = dict()
        self.finder = dict()
        self.identifier = 0
        return

    def get_user_by_id(self, id):
        return self.users.get(id)

    def get_user(self, name):
        id = self.finder.get(name)
        if id:
            return self.users.get(id)
        else:
            return None

    def save_user(self, user):
        self.users[user.id] = user
        self.finder[user.username] = user.id
        return

    def next_index(self):
        self.identifier += 1
        return self.identifier


users_repository = UsersRepository()


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if 'submit_button' in request.form:
            if request.form['submit_button'] == 'AddingOne':
                users_repository.users[
                    current_user.id].value += 1  # todo warp this as function.
            elif request.form['submit_button'] == 'MinusOne':
                users_repository.users[current_user.id].value -= 1
        return redirect(url_for('index'))
    else:
        return render_template(
            'index.html',
            username=current_user.username,
            value=users_repository.users[current_user.id].value)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_repository.get_user(username)
        if user:
            if user.password != password:
                return Response(
                    render_template("login_fail.html", username=username))
        else:
            user = User(username, password, users_repository.next_index())
            users_repository.save_user(user)
        login_user(user, remember=True)
        return redirect(url_for('index'))
    else:
        return Response(render_template("login.html"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)


if __name__ == '__main__':
    app.run()
