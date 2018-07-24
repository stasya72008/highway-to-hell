from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum, DATETIME

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('ID', Integer, primary_key=True)

    # ToDo(stasya) set varchar(255)
    name = Column('Username', String, nullable=False)

    def __init__(self, name):
        self.name = name


class Task(Base):
    __tablename__ = 'tasks'

    id = Column('ID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('users.id'))
    name = Column('Name', String, nullable=False)
    date = Column('Date', TIMESTAMP)
    status = Column('Status', Enum('active', 'done', 'deleted', 'archive'),
                    nullable=False, default='active')
    calendar_date = Column('Calendar_date', DATETIME)

    def __init__(self, user_id, name, date, status, calendar_date):
        self.user_id = user_id
        self.name = name
        self.date = date
        self.status = status
        self.calendar_date = calendar_date
