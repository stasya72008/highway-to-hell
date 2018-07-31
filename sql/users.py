from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql.entities import User

import config
from constants import sql_engine, use_db_query
from sql.helpers import entity_to_dict

conf = config.DBConfig()


class SQLUsers:
    def __init__(self):
        self.engine = create_engine(sql_engine.format(
            user=conf.user, password=conf.password, host=conf.host,
            port=conf.port), pool_size=2)

        with self.engine.begin() as conn:
            conn.execute(use_db_query)

        self.Session = sessionmaker(bind=self.engine)

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
