from django.db import models
from django.contrib.auth.models import User


# Decorator for field creation.
def make_field(fld_name, fld_obj, *args, **kwargs):
    def wrapper(cls):
        fk_field = fld_obj(*args, **kwargs)
        fk_field.contribute_to_class(cls, fld_name)
        return cls
    return wrapper


# Decorator for created datetime field.
def make_created_datetime():
    def wrapper(cls):
        return make_field('CreatedDateTime', models.DateTimeField, auto_now=True)(cls)
    return wrapper


# Decorator for owner field.
def make_owner(*args, **kwargs):
    def wrapper(cls):
        return make_field('User', models.ForeignKey, User, *args, **kwargs)(cls)
    return wrapper
