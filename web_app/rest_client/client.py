import requests
import json

import config

conf = config.RestEndpointConfig()

base_url = 'http://{host}:{port}/'.format(host=conf.host, port=conf.port)
user_tasks = base_url + 'users/{user_id}/tasks'
tasks_count = user_tasks + '/count'
task_url = base_url + 'tasks/{task_id}'
tasks_url = base_url + 'tasks'
users_url = base_url + 'users'
user_name_url = base_url + 'users/{user_name}'


def get_all_user_tasks(user_id):
    resp = requests.get(user_tasks.format(user_id=user_id))
    return json.loads(resp.text)


def get_task_by_id(task_id):
    resp = requests.get(task_url.format(task_id=task_id))
    return json.loads(resp.text)


def get_tasks_for_period(user_id, year=None, month=None, day=None):
    period = {'year': year, 'month': month, 'day': day}
    resp = requests.get(user_tasks.format(user_id=user_id), params=period)
    return json.loads(resp.text)


def get_task_count_for_period(user_id, year, month=None):
    period = {'year': year, 'month': month}
    resp = requests.get(tasks_count.format(user_id=user_id), params=period)
    return json.loads(resp.text)


def create_task(user_id, task_name, calendar_date=''):
    task = {'user_id': user_id,
            'name': task_name,
            'calendar_date': calendar_date}
    # ToDo(den) move user_id to init class rest_client after
    # https://github.com/stasya72008/highway-to-hell/projects/2#card-11180275
    return requests.post(tasks_url, json=json.dumps(task))


def delete_task(task_id):
    return requests.delete(task_url.format(task_id=task_id))


def edit_task(task_id, task_name='', calendar_date='', status='', position=0):
    data = {}
    if task_name:
        data['name'] = task_name
    if calendar_date:
        data['calendar_date'] = calendar_date
    if status:
        data['status'] = status
    if position:
        data['position'] = position
    resp = requests.put(task_url.format(task_id=task_id), json=data)
    return json.loads(resp.text)


def get_users():
    resp = requests.get(users_url)
    return json.loads(resp.text)


def get_user_by_name(user_name):
    resp = requests.get(user_name_url.format(user_name=user_name))
    return json.loads(resp.text)
