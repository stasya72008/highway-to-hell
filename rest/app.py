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
    added_user = sql_users.add_user(user['name'])
    return json.dumps(added_user), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sql_users.delete_user(user_id)
    return render_template('index.html'), 204


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = sql_users.get_user(user_id)
    return json.dumps(user) if user else not_found(404)


@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    """
    Get tasks for user with specified ID.
    Request args may be:
    empty - returns all user tasks
    period (in format year, [month], [day]) - return user tasks in accordance
    with this criteria

    :return: list of user tasks for the given period or all of the tasks
    """
    period = request.args
    if period:
        year = period['year']
        month = period.get('month', None)
        day = period.get('day', None)
        user_tasks = sql_tasks.get_tasks_for_period(user_id, year, month, day)
    else:
        user_tasks = sql_tasks.get_all_user_tasks(user_id)
    return json.dumps(user_tasks, default=str)


@app.route('/users/<int:user_id>/tasks/count', methods=['GET'])
def get_task_counts_for_period(user_id):
    period = request.args
    year = period['year']
    month = period.get('month', None)
    if month:
        tasks_count = sql_tasks.get_tasks_counts_for_month(
            user_id, year, month)
    else:
        tasks_count = sql_tasks.get_tasks_counts_for_year(user_id, year)
    tasks_count = {date: count for date, count in tasks_count}
    return json.dumps(tasks_count)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = sql_tasks.get_task(task_id)
    return json.dumps(task, default=str) if task else not_found(404)


@app.route('/tasks', methods=['POST'])
def add_task():
    # ToDo(stasya) Add json validation
    # https://github.com/stasya72008/highway-to-hell/projects/2#card-11155844
    task = json.loads(request.json)
    added_task = sql_tasks.add_task(task['user_id'], task['name'],
                                    task['calendar_date'])
    return json.dumps(added_task, default=str), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    sql_tasks.delete_task(task_id)
    return render_template('index.html'), 204


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data.get('name', '')
    calendar_date = data.get('calendar_date', None)
    status = data.get('status', None)
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
