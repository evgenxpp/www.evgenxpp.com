from django.db import models
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from webportal.lib.exceptions import AuthorizationRequired
from django.core.exceptions import FieldDoesNotExist


FIELD_CREATED_DATETIME = 'CreatedDateTime'
FIELD_REQUEST_CONTEXT = 'RequestContext'
FIELD_OWNER = 'Owner'


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
        return make_field(FIELD_CREATED_DATETIME, models.DateTimeField, auto_now=True)(cls)
    return wrapper


# Decorator for created user field.
def make_created_user(*args, **kwargs):
    fn_name = make_created_user.__name__

    def wrapper(cls):
        if not issubclass(cls, models.Model):
            raise Exception("%s: django.db.models.Model could be decorated only" % fn_name)

        meta = getattr(cls, "_meta", None)
        if not meta:
            raise Exception("%s: _meta object is not exists" % fn_name)

        try:
            meta.get_field(FIELD_REQUEST_CONTEXT)
        except FieldDoesNotExist:
            setattr(cls, FIELD_REQUEST_CONTEXT, None)
        else:
            raise ValueError("%s: %s field is already in use" % (fn_name, FIELD_REQUEST_CONTEXT))

        def save(self, *a, **kw):
            request = getattr(self, FIELD_REQUEST_CONTEXT, None)
            if isinstance(request, WSGIRequest) and request.user.is_authenticated():
                setattr(self, FIELD_OWNER, getattr(request, 'user'))
                super(self.__class__, self).save(*a, **kw)
            else:
                raise AuthorizationRequired("%s: authorization required for inserting into the %s table"
                                            % (fn_name, self.__class__.__name__))

        setattr(cls, save.__name__, save)

        return make_field(FIELD_OWNER, models.ForeignKey, User, *args, **kwargs)(cls)
    return wrapper
