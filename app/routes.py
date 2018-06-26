import json

from flask import render_template
from os import path

from app import app
from app.data import USER_TO_ADD, TASK_TO_ADD

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


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == int(user_id):
            users.remove(user)
        else:
            print ('My friends are gonna be there too')
    return json.dumps(users)


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == int(user_id):
            return json.dumps(user)
        else:
            return 'Oops'


@app.route('/users/<user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    user_tasks = list()
    for task in tasks:
        if task['user_id'] == int(user_id):
            user_tasks.append(task)

    return json.dumps(user_tasks)


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == int(task_id):
            return json.dumps(task)
        else:
            return 'Oops'


@app.route('/tasks', methods=['POST'])
def add_task():
    tasks.append(TASK_TO_ADD)
    return json.dumps(tasks)


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == int(task_id):
            tasks.remove(task)
        else:
            print ('Ain\'t nothin\' that I\'d rather do')
    return json.dumps(users)


@app.route('/users/<user_id>/tasks/<task_id>/actions/<action>', methods=['POST'])
def set_task_action():
    # TODO implement logic for actions
    pass
