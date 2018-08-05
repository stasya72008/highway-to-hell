from sql.entities import User
from sql.helpers import entity_to_dict
from sql.driver import SQlDriver

import config
conf = config.DBConfig()


class SQLUsers(SQlDriver):
    def __init__(self):
        SQlDriver.__init__(self)

    def add_user(self, user_name):
        session = self.Session()
        user = User(user_name)
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return entity_to_dict(user)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def update_user(self, user_id, user_name):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            user.name = user_name
            session.commit()
            session.refresh(user)
            return entity_to_dict(user)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_user(self, user_id):
        session = self.Session()
        try:
            session.query(User).filter_by(id=user_id).delete()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_user(self, user_id):
        session = self.Session()
        try:
            query = session.query(User).filter_by(id=user_id).first()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()

    def get_all_users(self):
        session = self.Session()
        try:
            query = session.query(User).all()
            return entity_to_dict(query)
        except:
            raise
        finally:
            session.close()
