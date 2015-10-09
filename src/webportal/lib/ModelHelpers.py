from django.db import models
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from webportal.lib.exceptions import AuthorizationRequired


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


# Decorator for created user field.
def make_created_user(request_field='RequestContext', user_field='Owner', *args, **kwargs):
    def wrapper(cls):
        meta = getattr(cls, "_meta", None)
        if not meta:
            raise Exception("Meta object is not exists")
        meta
        if not hasattr(cls, request_field):
            setattr(cls, request_field, None)
        else:
            raise ValueError('make_created_user: %s field is already in use' % request_field)

        def save(self, *a, **kw):
            request = getattr(self, request_field, None)
            if isinstance(request, WSGIRequest) and request.user.is_authenticated():
                setattr(self, user_field, getattr(request, 'user'))
                super(self.__class__, self).save(*a, **kw)
            else:
                raise AuthorizationRequired('Authorization required for inserting into the %s table.'
                                            % self.__class__.__name__)

        cls.save = save

        return make_field(user_field, models.ForeignKey, User, *args, **kwargs)(cls)
    return wrapper
