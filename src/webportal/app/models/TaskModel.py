from django.db import models
from django.contrib.auth.models import User as AuthUser
from webportal.app.models.AttachmentModel import AttachmentTable
from webportal.app.models.DiscussionModel import DiscussionTopicTable
from webportal.lib.ModelHelpers import make_created_user, make_created_datetime


@make_created_user()
@make_created_datetime()
class TaskTable(models.Model):
    TypeChoice = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
    )

    StatusChoice = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
    )

    Parent = models.ForeignKey("self")
    Shared = models.BooleanField()
    Type = models.IntegerField(choices=TypeChoice)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    PlanDate = models.DateField()
    Priority = models.SmallIntegerField()
    TechnicalInformation = models.TextField()
    Status = models.IntegerField(choices=StatusChoice)
    TimeStamp = models.DateTimeField()


class TaskUserTable(models.Model):
    Task = models.ForeignKey(TaskTable)
    User = models.ForeignKey(AuthUser)


class TaskAttachmentTable(models.Model):
    Task = models.ForeignKey(TaskTable)
    Attachment = models.ForeignKey(AttachmentTable)


class TaskDiscussionTable(models.Model):
    Task = models.ForeignKey(TaskTable)
    DiscussionTopic = models.ForeignKey(DiscussionTopicTable)

