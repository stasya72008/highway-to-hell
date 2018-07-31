from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from sql.entities import User
from sql.singleton import Singleton

conf = config.DBConfig()


class SQlDriver(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.engine = create_engine('mysql://{user}:{password}@{host}:{port}/highway'.format(
            user=conf.user, password=conf.password, host=conf.host, port=conf.port),
            pool_size=10)

        with self.engine.begin() as conn:
            conn.execute('use highway')

        self.Session = sessionmaker(bind=self.engine)
