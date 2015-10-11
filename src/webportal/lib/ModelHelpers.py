from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import FieldDoesNotExist
from webportal.lib.Exceptions import AuthorizationRequired

FIELD_OWNER = "Owner"
FIELD_TIMESTAMP = "TimeStamp"
FIELD_REQUEST_CONTEXT = "RequestContext"
FIELD_CREATED_DATETIME = "CreatedDateTime"


def _validate_class(cls, fn_name):
    if not issubclass(cls, models.Model):
        raise Exception("%s: django.db.models.Model could be decorated only" % fn_name)


def _field_exists(cls, fn_name, fld_name):
    meta = getattr(cls, "_meta", None)
    if not meta:
        raise Exception("%s: _meta object is not exists" % fn_name)

    try:
        meta.get_field(fld_name)
    except FieldDoesNotExist:
        return False

    return True


# Decorator for field creation.
def make_field(fn_name, fld_name, fld_obj, *args, **kwargs):
    def wrapper(cls):
        _validate_class(cls, fn_name)

        if _field_exists(cls, fn_name, fld_name):
            raise ValueError("%s: %s field is already in use" % (fn_name, fld_name))

        fk_field = fld_obj(*args, **kwargs)
        fk_field.contribute_to_class(cls, fld_name)

        return cls

    return wrapper


# Decorator for created datetime field.
def make_created_datetime():
    fn_name = make_created_datetime.__name__

    def wrapper(cls):
        return make_field(fn_name, FIELD_CREATED_DATETIME, models.DateTimeField, auto_now=True)(cls)

    return wrapper


# Decorator for timestamp field.
def make_time_stamp():
    fn_name = make_time_stamp.__name__

    def wrapper(cls):
        decorated_cls = make_field(fn_name, FIELD_TIMESTAMP, models.DateTimeField)(cls)

        def save(self, *args, **kwargs):
            setattr(self, FIELD_TIMESTAMP, datetime.utcnow())

            super(self.__class__, self).save(*args, **kwargs)

        setattr(decorated_cls, save.__name__, save)

        return decorated_cls

    return wrapper


# Decorator for created user field.
def make_created_user(*args, **kwargs):
    fn_name = make_created_user.__name__

    def wrapper(cls):
        decorated_cls = make_field(fn_name, FIELD_OWNER, models.ForeignKey, User, *args, **kwargs)(cls)

        if _field_exists(decorated_cls, fn_name, FIELD_REQUEST_CONTEXT):
            raise ValueError("%s: %s field is already in use" % (fn_name, FIELD_REQUEST_CONTEXT))
        else:
            setattr(decorated_cls, FIELD_REQUEST_CONTEXT, None)

        def save(self, *a, **kw):
            request = getattr(self, FIELD_REQUEST_CONTEXT, None)
            if not request:
                raise ValueError("%s: %s is empty" % (fn_name, FIELD_REQUEST_CONTEXT))

            if isinstance(request, WSGIRequest) and request.user.is_authenticated():
                setattr(self, FIELD_OWNER, getattr(request, "user"))
                super(self.__class__, self).save(*a, **kw)
            else:
                raise AuthorizationRequired("%s: authorization required for inserting into the %s table"
                                            % (fn_name, self.__class__.__name__))

        setattr(decorated_cls, save.__name__, save)

        return decorated_cls

    return wrapper
