from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum, DATETIME

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('ID', Integer, primary_key=True)
    name = Column('Username', String(length=255), nullable=False, unique=True)
    role = Column('Role', String(length=50), ForeignKey('roles.ID'))
    password = Column('Password', String(length=25), nullable=False)

    def __init__(self, name, pwd, role=None):
        self.name = name
        self.role = role if role else 2
        self.password = pwd


class Task(Base):
    __tablename__ = 'tasks'

    id = Column('ID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('users.ID'))
    name = Column('Name', String(length=255, convert_unicode=True,
                                 collation='utf8'), nullable=False)
    date = Column('Date', TIMESTAMP)
    status = Column('Status', Enum('active', 'done', 'deleted', 'archive'),
                    nullable=False, default='active')
    calendar_date = Column('Calendar_date', DATETIME, nullable=False,
                           default='0000-00-00 00:00:00')
    position = Column('Position', Integer, nullable=False)

    def __init__(self, user_id, name, calendar_date, position=None):
        self.user_id = user_id
        self.name = name
        self.calendar_date = calendar_date
        self.position = position if position else 999999


class Role(Base):
    __tablename__ = 'roles'

    id = Column('ID', Integer, primary_key=True)
    role_name = Column('Role', String(50), nullable=False)
