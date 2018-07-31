from flask import Flask, render_template
import json
import config

from flask import request

from sql.tasks import SQLTasks
from sql.users import SQLUsers

app = Flask(__name__)


config = config.RestConfig()
sql_users = SQLUsers()
sql_tasks = SQLTasks()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def get_users():
    return json.dumps(sql_users.get_all_users())


@app.route('/users', methods=['POST'])
def add_user():
    user = json.loads(request.json)
    user_name = user['name']
    added_user = sql_users.add_user(user_name)
    return json.dumps(added_user), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sql_users.delete_user(user_id)
    return render_template('index.html'), 204


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = sql_users.get_user(user_id)
    if user:
        return json.dumps(user)
    return not_found(404)


@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    period = request.args
    month = None
    day = None
    if period:
        year = period['year']
        if 'month' in period:
            month = period['month']
        if 'day' in period:
            day = period['day']
        user_tasks = sql_tasks.get_tasks_for_period(user_id, year, month, day)
    else:
        user_tasks = sql_tasks.get_all_user_tasks(user_id)
    return json.dumps(user_tasks, default=str)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = sql_tasks.get_task(task_id)
    if task:
        return json.dumps(task)
    return not_found(404)


@app.route('/tasks', methods=['POST'])
def add_task():
    # ToDo(stasya) Add json validation
    # https://github.com/stasya72008/highway-to-hell/projects/2#card-11155844
    task = json.loads(request.json)
    user_id = task['user_id']
    name = task['name']
    calendar_date = task['calendar_date']
    added_task = sql_tasks.add_task(user_id, name, calendar_date)
    return json.dumps(added_task, default=str), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    sql_tasks.delete_task(task_id)
    return render_template('index.html'), 204


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    name = ''
    status = None
    calendar_date = None
    data = request.json
    if 'name' in data:
        name = data['name']
    if 'calendar_date' in data:
        calendar_date = data['calendar_date']
    if 'status' in data:
        status = data['status']
    updated_task = sql_tasks.update_task(task_id, name, status, calendar_date)
    return json.dumps(updated_task, default=str)


@app.route('/users/<int:user_id>/tasks/<int:task_id>/actions/<action>', methods=['POST'])
def set_task_action():
    # TODO implement logic for actions
    pass


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(host=config.host, port=int(config.port), debug=config.debug)
