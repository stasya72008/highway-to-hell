from flask import Flask, render_template
from os import path
import json

from rest.data.data import USER_TO_ADD

app = Flask(__name__)

from app import app


data_dir = path.join(path.dirname(__file__), 'data')
users_data = path.join(data_dir, 'users.json')
tasks_data = path.join(data_dir, 'tasks.json')

users = json.loads(open(users_data).read())
tasks = json.loads(open(tasks_data).read())


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', users=users, tasks=tasks)


@app.route('/users', methods=['GET'])
def get_users():
    return json.dumps(users)


@app.route('/users', methods=['POST'])
def add_user():
    users.append(USER_TO_ADD)
    return json.dumps(users)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return json.dumps(users)
    return not_found(404)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return json.dumps(user)
    return not_found(404)


@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id, start='', end=''):
    # ToDo(stasya): add request to database
    user_tasks = list()
    for task in tasks:
        if task['user_id'] == user_id:
            # SQL request for the given period
            user_tasks.append(task)

    return json.dumps(user_tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return json.dumps(task)
    return not_found(404)


@app.route('/tasks', methods=['POST'])
def add_task(task):
    tasks.append(task)
    return render_template('index.html'), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return json.dumps(tasks)
    return not_found(404)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id, **kwargs):
    # ToDo(stasya) add logic for updating values for existing keys
    # add check whether key is in kwargs
    for task in tasks:
        if task['id'] == task_id:
            for item in kwargs:
                item = dict([item])
                task.update(item)
            return json.dumps(task)
    return not_found(404)


@app.route('/users/<int:user_id>/tasks/<int:task_id>/actions/<action>', methods=['POST'])
def set_task_action():
    # TODO implement logic for actions
    pass


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
