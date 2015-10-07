from django.db import models
from django.contrib.auth.models import User


class TaskTable(models.Model):
    TypeChoice = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
    )

    Owner = models.ForeignKey(User)
    CreatedDateTime = models.DateTimeField(auto_now=True)
    Parent = models.ForeignKey('self')
    Shared = models.BooleanField()
    Type = models.IntegerField(choices=TypeChoice)
    Name = models.CharField()
    Description = models.TextField()
    PlanDate = models.DateField()
    Priority = models.SmallIntegerField()
    TechnicalInformation = models.TextField()

