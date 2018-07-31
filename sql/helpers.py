def entity_to_dict(query_result):
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
