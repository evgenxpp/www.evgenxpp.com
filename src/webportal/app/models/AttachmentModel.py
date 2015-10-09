from django.db import models
from webportal.lib.ModelHelpers import make_created_user, make_created_datetime


@make_created_user()
@make_created_datetime()
class AttachmentTable(models.Model):
    Name = models.CharField(max_length=255)
    File = models.FileField()

