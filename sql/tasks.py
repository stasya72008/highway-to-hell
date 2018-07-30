from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
from sql.entities import Task

import config
from constants import sql_engine, use_db_query
from sql.helpers import entity_to_dict

conf = config.DBConfig()


#Todo(stasya) add logging to except blocks
class SQLTasks:
    def __init__(self):
        self.engine = create_engine(sql_engine.format(
            user=conf.user, password=conf.password, host=conf.host,
            port=conf.port), pool_size=2)

        with self.engine.begin() as conn:
            conn.execute(use_db_query)

        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, user_id, name, status=None, calendar_date=None):
        session = self.Session()
        task = Task(user_id, name, status, calendar_date)
        try:
            session.add(task)
            session.commit()
            query = session.query(Task).filter_by(id=task.id).first()
            return entity_to_dict(query)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def update_task(self, task_id, name='', status=None, calendar_date=None):
        session = self.Session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if name:
                task.name = name
            if status:
                task.status = status
            if calendar_date:
                task.calendar_date = calendar_date
            session.commit()
            query = session.query(Task).filter_by(id=task.id).first()
            return entity_to_dict(query)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_task(self, task_id):
        session = self.Session()
        try:
            session.query(Task).filter_by(id=task_id).delete()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_task(self, task_id):
        session = self.Session()
        try:
            query = session.query(Task).filter_by(id=task_id).first()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()

    def get_all_user_tasks(self, user_id):
        session = self.Session()
        try:
            query = session.query(Task).filter_by(user_id=user_id).all()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()

    def get_existing_user_tasks(self, user_id):
        session = self.Session()
        try:
            query = session.query(Task).filter_by(user_id=user_id).filter(
                Task.status != 'deleted').all()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()

    def get_task_by_date(self, user_id, date):
        session = self.Session()
        try:
            query = session.query(Task).filter_by(user_id=user_id).filter(
                Task.calendar_date == date).all()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()

    def get_tasks_for_period(self, user_id, year, month=None, day=None):
        session = self.Session()
        try:
            query = session.query(Task).filter_by(user_id=user_id).filter(
                        extract('year', Task.calendar_date) == year,
                        True if month is None else
                        (extract('month', Task.calendar_date) == month),
                        True if day is None else
                        (extract('day', Task.calendar_date) == day)).all()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()
