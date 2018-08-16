from sql.entities import User
from sql.helpers import entity_to_dict, helper_session
from sql.driver import SQlDriver

import config
conf = config.DBConfig()


class SQLUsers(SQlDriver):
    def __init__(self):
        SQlDriver.__init__(self)

    @helper_session
    def add_user(self, user_name, password, role=None):
        user = User(user_name, password, role)
        self.temp_session.add(user)
        self.temp_session.commit()
        self.temp_session.refresh(user)
        return entity_to_dict(user)

    @helper_session
    def update_user(self, user_id, user_name, role, password):
        user = self.temp_session.query(User).filter_by(id=user_id).first()
        if user_name:
            user.name = user_name
        if role:
            user.role = role
        if password:
            user.password = password
            self.temp_session.commit()
            self.temp_session.refresh(user)
        return entity_to_dict(user)

    @helper_session
    def delete_user(self, user_id):
        self.temp_session.query(User).filter_by(id=user_id).delete()
        self.temp_session.commit()

    @helper_session
    def get_user(self, user_id):
        query = self.temp_session.query(User).filter_by(id=user_id).first()
        return entity_to_dict(query)

    @helper_session
    def get_all_users(self):
        query = self.temp_session.query(User).all()
        return entity_to_dict(query)

    @helper_session
    def get_user_by_name(self, username):
        query = self.temp_session.query(User).filter_by(name=username).first()
        return entity_to_dict(query)
