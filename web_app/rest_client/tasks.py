from rest import app
import json


def get_all_user_tasks(user_id):
    return json.loads(app.get_user_tasks(user_id))


def get_task_by_id(task_id):
    return json.loads(app.get_task(task_id))


def get_tasks_for_period(user_id, start, end):
    return json.loads(app.get_user_tasks(user_id, start, end))


def create_task(task):
    app.add_task(task)


def delete_task(task_id):
    return json.loads(app.delete_task(task_id))


def edit_task(task_id, **kwargs):
    return json.loads(app.update_task(task_id, kwargs))
