from django.db import models
from webportal.lib.ModelHelpers import make_owner, make_created_datetime


@make_owner()
@make_created_datetime()
class TaskTable(models.Model):
    TypeChoice = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
    )

    Parent = models.ForeignKey('self')
    Shared = models.BooleanField()
    Type = models.IntegerField(choices=TypeChoice)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    PlanDate = models.DateField()
    Priority = models.SmallIntegerField()
    TechnicalInformation = models.TextField()
