from sqlalchemy import extract
from sqlalchemy import func
from sqlalchemy import or_

import logging

from sql.entities import Task
from sql.helpers import entity_to_dict, helper_session
from sql.driver import SQlDriver

import config
conf = config.DBConfig()
config.LogConfig()
logger = logging.getLogger("SQL")


class SQLTasks(SQlDriver):
    def __init__(self):
        SQlDriver.__init__(self)

    @helper_session
    def add_task(self, user_id, name, calendar_date=''):
        logger.info('Adding new task to database: "%s"' % name)
        task = Task(user_id, name, calendar_date)
        self.temp_session.add(task)
        self.temp_session.commit()
        self.temp_session.refresh(task)
        logger.info('Query OK')
        return entity_to_dict(task)

    @helper_session
    def update_task(self, task_id, name='', status=None, calendar_date='',
                    position=0):       
        task = self.temp_session.query(Task).filter_by(id=task_id).first()
        logger.info('Updating task with id "%s" in database' % task_id)
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
        logger.info('Query OK')
        return entity_to_dict(task)

    @helper_session
    def delete_task(self, task_id):
        logger.info('Deleting task with id "%s" in database' % task_id)
        self.temp_session.query(Task).filter_by(id=task_id).delete()
        self.temp_session.commit()

    @helper_session
    def get_task(self, task_id):
        logger.info('Get task with id "%s"' % task_id)
        query = self.temp_session.query(Task).filter_by(id=task_id).first()
        return entity_to_dict(query)

    @helper_session
    def get_all_user_tasks(self, user_id):
        logger.info('Get all tasks for user_id "%s"' % user_id)
        query = self.temp_session.query(Task).filter_by(user_id=user_id).all()
        return entity_to_dict(query)

    @helper_session
    def get_existing_user_tasks(self, user_id):
        logger.info('Get all not deleted tasks for user_id "% s" in database' %
                    user_id)
        query = self.temp_session.query(Task).filter_by(user_id=user_id).filter(
            Task.status != 'deleted').all()
        return entity_to_dict(query)

    @helper_session
    def get_tasks_for_period(self, user_id, year, month=None, day=None):
        logger.info('Get tasks for user_id "{user_id}" for year={year}, '
                    'month={month}, day={day}'.format(user_id=user_id,
                                                      year=year, month=month,
                                                      day=day))
        query = self.temp_session.query(Task).filter_by(user_id=user_id).filter(
                    extract('year', Task.calendar_date) == year,
                    True if month is None else
                    (extract('month', Task.calendar_date) == month),
                    True if day is None else
                    (extract('day', Task.calendar_date) == day)).all()
        return entity_to_dict(query)

    @helper_session
    def get_tasks_counts_for_year(self, user_id, year):
        logger.info('Get months task counts for year %s for user_id "%s"' %
                    (year, user_id))
        query = self.temp_session.query(
            func.month(Task.calendar_date), func.count(Task.calendar_date))\
            .filter_by(user_id=user_id)\
            .filter(extract('year', Task.calendar_date) == year)\
            .filter(or_(Task.status == 'active', Task.status == 'done'))\
            .group_by(func.month(Task.calendar_date)).all()
        return query

    @helper_session
    def get_tasks_counts_for_month(self, user_id, year, month):
        logger.info('Get days task counts for month %s, year %s for user_id "%s"' %
                    (month, year, user_id))
        query = self.temp_session.query(
            func.day(Task.calendar_date), func.count(Task.calendar_date))\
            .filter_by(user_id=user_id).filter(
                    extract('year', Task.calendar_date) == year,
                    extract('month', Task.calendar_date) == month) \
            .filter(or_(Task.status == 'active', Task.status == 'done')) \
            .group_by(func.day(Task.calendar_date)).all()
        return query
