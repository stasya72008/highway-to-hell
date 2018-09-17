from flask import Flask, render_template
import json
import pprint
import config

from flask import request

from sql.tasks import SQLTasks
from sql.users import SQLUsers
import logging

app = Flask(__name__)

config.LogConfig()
logger = logging.getLogger("rest")

config = config.RestConfig()
sql_users = SQLUsers()
sql_tasks = SQLTasks()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def get_users():
    logger.info('Get all existing users')
    return json.dumps(sql_users.get_all_users())


@app.route('/users', methods=['POST'])
def add_user():
    user = json.loads(request.json)
    logger.info('Creating new user "%s"' % user['name'])
    added_user = sql_users.add_user(user['name'])
    logger.debug('New user: %s' % pprint.pformat(added_user))
    return json.dumps(added_user), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    logger.info('Deleting user with id "%s"' % user_id)
    sql_users.delete_user(user_id)
    return render_template('index.html'), 204


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    logger.info('Getting user with id "%s"' % user_id)
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
        logger.info('Get tasks for user_id "{}" for year={}, month={}, day={}'
                    .format(user_id, year, month,day))
        user_tasks = sql_tasks.get_tasks_for_period(user_id, year, month, day)
    else:
        user_tasks = sql_tasks.get_all_user_tasks(user_id)
    logger.debug('Tasks list: %s' % pprint.pformat(user_tasks))
    return json.dumps(user_tasks, default=str)


@app.route('/users/<string:user_name>', methods=['GET'])
def get_user_by_name(user_name):
    logger.info('Getting user with name "%s"' % user_name)
    user = sql_users.get_user_by_name(user_name)
    return json.dumps(user) if user else not_found(404)


@app.route('/users/<int:user_id>/tasks/count', methods=['GET'])
def get_task_counts_for_period(user_id):
    period = request.args
    year = period['year']
    month = period.get('month', None)
    logger.info('Get tasks count for period year={year}, month={month}'.format(
        year=year, month=month))
    if month:
        tasks_count = sql_tasks.get_tasks_counts_for_month(
            user_id, year, month)
    else:
        tasks_count = sql_tasks.get_tasks_counts_for_year(user_id, year)
    logger.debug('Tasks count: %s' % pprint.pformat(tasks_count))
    tasks_count = {date: count for date, count in tasks_count}
    return json.dumps(tasks_count)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    logger.info('Getting task with id "%s"' % task_id)
    task = sql_tasks.get_task(task_id)
    return json.dumps(task, default=str) if task else not_found(404)


@app.route('/tasks', methods=['POST'])
def add_task():
    # ToDo(stasya) Add json validation
    # https://github.com/stasya72008/highway-to-hell/projects/2#card-11155844
    task = json.loads(request.json)
    logger.info('Creating new task %s' % pprint.pformat(task))
    added_task = sql_tasks.add_task(task['user_id'], task['name'],
                                    task['calendar_date'])
    return json.dumps(added_task, default=str), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    logger.info('Deleting task with id "%s"' % task_id)
    sql_tasks.delete_task(task_id)
    return render_template('index.html'), 204


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    logger.info('Updating task with id "%s". New values: %s' % (task_id, data))
    name = data.get('name', '')
    calendar_date = data.get('calendar_date', None)
    status = data.get('status', None)
    updated_task = sql_tasks.update_task(task_id, name, status, calendar_date)
    logger.debug('Updated task: %s' % pprint.pformat(updated_task))
    return json.dumps(updated_task, default=str)


@app.route('/users/<int:user_id>/tasks/<int:task_id>/actions/<action>', methods=['POST'])
def set_task_action():
    # TODO implement logic for actions
    pass


@app.errorhandler(404)
def not_found(error):
    logger.error('Requested object was not found!')
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(host=config.host, port=int(config.port), debug=config.debug)
