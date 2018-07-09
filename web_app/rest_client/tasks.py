import requests
import json

import data.data_templates as template

# ToDo(stasya) Move base_url to config after
# https://github.com/stasya72008/highway-to-hell/projects/2#card-11155636
base_url = 'http://localhost:5000/'
user_tasks = base_url + 'users/{user_id}/tasks'
task_url = base_url + 'tasks/{task_id}'
tasks_url = base_url + 'tasks'


def get_all_user_tasks(user_id):
    resp = requests.get(user_tasks.format(user_id=user_id))
    return json.loads(resp.text)


def get_task_by_id(task_id):
    resp = requests.get(task_url.format(task_id=task_id))
    return json.loads(resp.text)


def get_tasks_for_period(user_id, start, end):
    period = {'start': start, 'end': end}
    resp = requests.get(user_tasks.format(user_id=user_id), params=period)
    return json.loads(resp.text)


def create_task(user_id, task_name, date, status=''):
    task = template.task
    task['user_id'] = user_id
    task['name'] = task_name
    task['date'] = date
    task['status'] = status if status else 'active'
    return requests.post(tasks_url, json=json.dumps(task))


def delete_task(task_id):
    return requests.delete(task_url.format(task_id=task_id))


def edit_task(task_id, task_name='', date=''):
    data = {}
    if task_name:
        data['name'] = task_name
    if date:
        data['date'] = date
    resp = requests.put(task_url.format(task_id=task_id), json=data)
    return json.loads(resp.text)
