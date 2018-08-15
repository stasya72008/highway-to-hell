from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import or_

from sql.entities import Task
from sql.helpers import entity_to_dict, helper_session
from sql.driver import SQlDriver

import config
conf = config.DBConfig()


#Todo(stasya) add logging to except blocks
class SQLTasks(SQlDriver):
    def __init__(self):
        SQlDriver.__init__(self)

    @helper_session
    def add_task(self, user_id, name, calendar_date=''):
        task = Task(user_id, name, calendar_date)
        self.temp_session.add(task)
        self.temp_session.commit()
        self.temp_session.refresh(task)
        return entity_to_dict(task)

    @helper_session
    def update_task(self, task_id, name='', status=None, calendar_date='',
                    position=0):       
        task = self.temp_session.query(Task).filter_by(id=task_id).first()
        if name:
            task.name = name
        if status:
            task.status = status
        if calendar_date:
            task.calendar_date = calendar_date
        if position:
            task.position = position
        self.temp_session.commit()
        self.temp_session.refresh(task)
        return entity_to_dict(task)

    @helper_session
    def delete_task(self, task_id):
        self.temp_session.query(Task).filter_by(id=task_id).delete()
        self.temp_session.commit()

    @helper_session
    def get_task(self, task_id):
        query = self.temp_session.query(Task).filter_by(id=task_id).first()
        return entity_to_dict(query)

    @helper_session
    def get_all_user_tasks(self, user_id):
        query = self.temp_session.query(Task).filter_by(user_id=user_id).all()
        return entity_to_dict(query)

    @helper_session
    def get_existing_user_tasks(self, user_id):
        query = self.temp_session.query(Task).filter_by(user_id=user_id).filter(
            Task.status != 'deleted').all()
        return entity_to_dict(query)

    @helper_session
    def get_tasks_for_period(self, user_id, year, month=None, day=None):
        query = self.temp_session.query(Task).filter_by(user_id=user_id).filter(
                    extract('year', Task.calendar_date) == year,
                    True if month is None else
                    (extract('month', Task.calendar_date) == month),
                    True if day is None else
                    (extract('day', Task.calendar_date) == day)).all()
        return entity_to_dict(query)

    @helper_session
    def get_tasks_counts_for_year(self, user_id, year):
        query = self.temp_session.query(
            func.month(Task.calendar_date), func.count(Task.calendar_date))\
            .filter_by(user_id=user_id)\
            .filter(extract('year', Task.calendar_date) == year)\
            .filter(or_(Task.status == 'active', Task.status == 'done'))\
            .group_by(func.month(Task.calendar_date)).all()
        return query

    @helper_session
    def get_tasks_counts_for_month(self, user_id, year, month):
        query = self.temp_session.query(
            func.day(Task.calendar_date), func.count(Task.calendar_date))\
            .filter_by(user_id=user_id).filter(
                    extract('year', Task.calendar_date) == year,
                    extract('month', Task.calendar_date) == month) \
            .filter(or_(Task.status == 'active', Task.status == 'done')) \
            .group_by(func.day(Task.calendar_date)).all()
        return query
