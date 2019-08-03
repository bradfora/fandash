import pymongo

from FantasyForecaster.dao.query import SortOrder, Operation, ComparisonOperator

# todo write tests

_comp_map = {
    ComparisonOperator.EQ: None,
    ComparisonOperator.GT: '$gt',
    ComparisonOperator.LT: '$lt',
}

_sort_map = {
    SortOrder.ASC: pymongo.ASCENDING,
    SortOrder.DESC: pymongo.DESCENDING,
}


_op_map = {
    Operation.SET: '$set',
    Operation.SET_DATE: '$currentDate',
    Operation.INC: '$inc',
    Operation.MIN: '$min',
    Operation.MAX: '$max',
    Operation.MUL: '$mul',
    Operation.RENAME: '$rename',
    Operation.SET_ON_INSERT: '$setOnInsert',
    Operation.UNSET: '$unset',
}


# todo also handle the case when the operator is the Mongo specific operator just in case
def comparison(field, operator, value):
    """Formats a mongoDB query condition field (< | > | ==) value"""
    if operator in [ComparisonOperator.EQ, ComparisonOperator.EQ.value]:
        return {field: value}
    elif operator in [ComparisonOperator.LT, ComparisonOperator.LT.value, _comp_map[ComparisonOperator.LT]]:
        return {field: {"$lt": value}}
    elif operator in [ComparisonOperator.GT, ComparisonOperator.GT.value, _comp_map[ComparisonOperator.GT]]:
        return {field: {"$gt": value}}
    else:
        raise ValueError('Unexpected value {} in MongoDB comparison operator'.format(operator))


def and_conditions(*conds):
    """Formats a list of conditions into a mongoDB logical AND statement"""
    return {key: val for cond in conds for key, val in cond}


def or_conditions(*conds):
    """Formats a list of conditions into a mongoDB logical OR statement"""
    return {"$or": conds}


def sort(sort_dict):
    """dict should have key = field name : val = sort_order (asc | desc)"""
    return [(field, _map_to_mongo(_sort_map, sort_order)) for field, sort_order in sort_dict]


# todo validate that this still works after refactor, some ops used to be {field, value} not {field: value}
def format_update(mods_tuples):
    """formats mongoDB update arguments from a tuple of operation, field, value"""
    return {_map_to_mongo(_op_map, op): {field: value} for op, field, value in mods_tuples}


def _map_to_mongo(mongo_map, enum_val):
    try:
        return mongo_map[enum_val]
    except KeyError:
        raise NotImplementedError('Unsupported operation ({}) for MongoDB implementation.'.format(enum_val.name))
