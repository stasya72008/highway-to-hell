from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql.entities import User

import config

conf = config.DBConfig()


class SQLUsers:
    def __init__(self):
        self.engine = create_engine('mysql://{user}:{password}@{host}:{port}/highway'.format(
            user=conf.user, password=conf.password, host=conf.host, port=conf.port),
            pool_size=2)

        with self.engine.begin() as conn:
            conn.execute('use highway')

        self.Session = sessionmaker(bind=self.engine)

    # def __init__(self):
    #     # super(SQLUsers, self).__init__()
    #     metadata = MetaData()
    #     self.users = Table(User, metadata)

    def add_user(self, user_name):
        session = self.Session()
        user = User(user_name)
        try:
            session.add(user)
            session.commit()
            return session.query(User).filter_by(id=user.id).first()
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
            return session.query(User).filter_by(id=user_id).first()
        except:
            raise
        finally:
            session.close()
