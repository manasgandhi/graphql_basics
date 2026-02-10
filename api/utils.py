def get_requested_fields(info):
    return {field.name.value for field in info.field_nodes[0].selection_set.selections}
