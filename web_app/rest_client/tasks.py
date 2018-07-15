import requests
import json

import config
import data.data_templates as template

conf = config.RestConfig()

base_url = 'http://{host}:{port}/'.format(host=conf.host, port=conf.port)
user_tasks = base_url + 'users/{user_id}/tasks'
task_url = base_url + 'tasks/{task_id}'
tasks_url = base_url + 'tasks'

tasks = [
    {
        "user_id": 1,
        "id": 1,
        "name": "Livin' 1",
        "date": "today",
        "status": "active",
        "calendar_date": "2018|1|1|0"
    },
    {
        "user_id": 1,
        "id": 2,
        "name": "Livin' 2",
        "date": "today",
        "status": "active",
        "calendar_date": "2018|1|1|0"
    },
    {
        "user_id": 1,
        "id": 3,
        "name": "Livin' 3",
        "date": "today",
        "status": "delete",
        "calendar_date": "2018|1|1|0"
    },
    {
        "user_id": 1,
        "id": 33,
        "name": "Livin' 33",
        "date": "today",
        "status": "done",
        "calendar_date": "2018|1|1|3"
    },
    {
        "user_id": 1,
        "id": 4,
        "name": "Livin' 4",
        "date": "today",
        "status": "done",
        "calendar_date": "2018|1|2|0"
    },
    {
        "user_id": 1,
        "id": 5,
        "name": "Livin' 5",
        "date": "today",
        "status": "active",
        "calendar_date": "2018|2|2|0"
    }
]

def get_all_user_tasks(user_id):
    # resp = requests.get(user_tasks.format(user_id=user_id))
    return tasks


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
