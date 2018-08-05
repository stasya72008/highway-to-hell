from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import sql_engine, use_db_query


import config
from sql.singleton import Singleton

conf = config.DBConfig()


class SQlDriver(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.engine = create_engine(sql_engine.format(
            user=conf.user, password=conf.password, host=conf.host,
            port=conf.port), pool_size=5)

        with self.engine.begin() as conn:
            conn.execute(use_db_query)

        self.Session = sessionmaker(bind=self.engine)
