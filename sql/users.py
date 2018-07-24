from sqlalchemy import MetaData
from sqlalchemy import Table

from sql.entities import User

from sql.driver import SQlDriver


class SQLUsers(SQlDriver):
    def __init__(self):
        super(SQLUsers, self).__init__()
        metadata = MetaData()
        self.users = Table(User, metadata)

    def add_user(self, user_name):
        session = self.Session()
        user = User(user_name)
        try:
            session.add(user)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        #Todo(stasya) return User obj

    def update_user(self, user_id, user_name):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            user.name = user_name
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

if __name__ == '__main__':
    a = SQLUsers().update_user(3, 'azaza')

