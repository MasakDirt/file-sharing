from sqlalchemy import inspect


def serialize_obj(obj: object) -> dict:
    return {
        value.key: getattr(obj, value.key)
        for value in inspect(obj).mapper.column_attrs
    }
