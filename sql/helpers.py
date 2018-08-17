def entity_to_dict(query_result):
    if query_result is None:
        return dict()

    if isinstance(query_result, list):
        result = []
        for row in query_result:
            attr_dict = row.__dict__
            attr_dict.pop('_sa_instance_state', None)
            result.append(attr_dict)
    else:
        result = query_result.__dict__
        result.pop('_sa_instance_state', None)
    return result


def helper_session(func):
    def wrapper(self, *args, **kwargs):
        self.temp_session = self.Session()
        try:
            return func(self, *args, **kwargs)
        except:
            self.temp_session.rollback()
            raise
        finally:
            self.temp_session.close()
    return wrapper

