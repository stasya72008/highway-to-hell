from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum, DATETIME

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('ID', Integer, primary_key=True)
    name = Column('Username', String(length=255), nullable=False)

    def __init__(self, name):
        self.name = name


class Task(Base):
    __tablename__ = 'tasks'

    id = Column('ID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('users.ID'))
    name = Column('Name', String(length=255), nullable=False)
    date = Column('Date', TIMESTAMP)
    status = Column('Status', Enum('active', 'done', 'deleted', 'archive'),
                    nullable=False, default='active')
    calendar_date = Column('Calendar_date', DATETIME)

    def __init__(self, user_id, name, status, calendar_date):
        self.user_id = user_id
        self.name = name
        self.status = status
        self.calendar_date = calendar_date
