from sql.entities import User
from sql.helpers import entity_to_dict, helper_session
from sql.driver import SQlDriver
import logging

import config
conf = config.DBConfig()
config.LogConfig()
logger = logging.getLogger("SQL")


class SQLUsers(SQlDriver):
    def __init__(self):
        SQlDriver.__init__(self)

    @helper_session
    def add_user(self, user_name, password, role=None):
        logger.info('Adding new user to database: %s' % user_name)
        user = User(user_name, password, role)
        logger.debug('User info: %s' % user)
        self.temp_session.add(user)
        self.temp_session.commit()
        self.temp_session.refresh(user)
        return entity_to_dict(user)

    @helper_session
    def update_user(self, user_id, user_name, role, password):
        user = self.temp_session.query(User).filter_by(id=user_id).first()
        logger.info('Updating user with id %s in database' % user_id)
        logger.debug('Old user: %s' % user)
        if user_name:
            user.name = user_name
        if role:
            user.role = role
        if password:
            user.password = password
        logger.debug('New user: %s' % user)
        self.temp_session.commit()
        self.temp_session.refresh(user)
        return entity_to_dict(user)

    @helper_session
    def delete_user(self, user_id):
        logger.info('Deleting user with id %s in database' % user_id)
        self.temp_session.query(User).filter_by(id=user_id).delete()
        self.temp_session.commit()

    @helper_session
    def get_user(self, user_id):
        logger.info('Get user with id %s' % user_id)
        query = self.temp_session.query(User).filter_by(id=user_id).first()
        return entity_to_dict(query)

    @helper_session
    def get_all_users(self):
        logger.info('Get all users in database')
        query = self.temp_session.query(User).all()
        return entity_to_dict(query)

    @helper_session
    def get_user_by_name(self, username):
        logger.info('Get user with name %s' % username)
        query = self.temp_session.query(User).filter_by(name=username).first()
        return entity_to_dict(query)
