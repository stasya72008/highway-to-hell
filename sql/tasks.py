from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
from sql.entities import Task

import config
from constants import sql_engine, use_db_query

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
            return session.query(Task).filter_by(id=task.id).first()
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
            return session.query(Task).filter_by(id=task_id).first()
        except:
            raise
        finally:
            session.close()

    def get_all_user_tasks(self, user_id):
        session = self.Session()
        try:
            return session.query(Task).filter_by(user_id=user_id).all()
        except:
            raise
        finally:
            session.close()

    def get_existing_user_tasks(self, user_id):
        session = self.Session()
        try:
            return session.query(Task).filter_by(user_id=user_id).filter(
                Task.status != 'deleted').all()
        except:
            raise
        finally:
            session.close()

    def get_task_by_date(self, user_id, date):
        session = self.Session()
        try:
            return session.query(Task).filter_by(user_id=user_id).filter(
                Task.calendar_date == date).all()
        except:
            raise
        finally:
            session.close()

    def get_tasks_for_period(self, user_id, year, month=None, day=None):
        session = self.Session()
        selection_clause = str(year)
        extraction_param = 'year'

        if month:
            extraction_param = 'year_month'
            month = str(month)
            if len(month) == 1:
                month = '0{}'.format(month)
            selection_clause += month
        try:
            query = session.query(Task).filter_by(user_id=user_id).filter(
                    extract(extraction_param,
                            Task.calendar_date) == selection_clause)
            if not day:
                return query.all()
            else:
                return query.filter(
                    extract('day', Task.calendar_date) == day).all()
        except:
            raise
        finally:
            session.close()

    def get_tasks_for_period2(self, user_id, year, month=None, day=None):
        session = self.Session()
        tasksss = session.query(Task).filter_by(user_id=user_id).filter(
            extract('year', Task.calendar_date) == year,
            True if month is None else
                (extract('month', Task.calendar_date) == month),
            True if day is None else
                (extract('day', Task.calendar_date) == day)).all()
        session.close()

        return tasksss

import pprint
qqq = SQLTasks()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint([t.calendar_date for t in qqq.get_all_user_tasks(5)])

assert len(qqq.get_tasks_for_period(5, 2018)) == \
       len(qqq.get_tasks_for_period2(5, 2018))

assert len(qqq.get_tasks_for_period(5, 2018, 7)) == \
       len(qqq.get_tasks_for_period2(5, 2018, 7))

assert len(qqq.get_tasks_for_period(5, 2018, 7, 15)) == \
       len(qqq.get_tasks_for_period2(5, 2018, 7, 15))
