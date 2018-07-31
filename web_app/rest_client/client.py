import requests
import json
import random

import config
import data.data_templates as template

conf = config.RestEndpointConfig()

base_url = 'http://{host}:{port}/'.format(host=conf.host, port=conf.port)
user_tasks = base_url + 'users/{user_id}/tasks'
task_url = base_url + 'tasks/{task_id}'
tasks_url = base_url + 'tasks'


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


def create_task(user_id, task_name, calendar_date=None):
    task = dict()
    # ToDo(den) move user_id to init class rest_client after
    # https://github.com/stasya72008/highway-to-hell/projects/2#card-11180275
    task['user_id'] = user_id
    task['name'] = task_name
    task['calendar_date'] = calendar_date
    task['id'] = random.randint(10, 1000000)
    return requests.post(tasks_url, json=json.dumps(task))


def delete_task(task_id):
    return requests.delete(task_url.format(task_id=task_id))


def edit_task(task_id, task_name='', calendar_date='', status=''):
    data = {}
    if task_name:
        data['name'] = task_name
    if calendar_date:
        data['calendar_date'] = calendar_date
    if status:
        data['status'] = status
    resp = requests.put(task_url.format(task_id=task_id), json=data)
    return json.loads(resp.text)
