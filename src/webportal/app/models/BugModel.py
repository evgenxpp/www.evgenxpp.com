from django.db import models
from webportal.app.models.TaskModel import TaskTable
from webportal.app.models.AttachmentModel import AttachmentTable
from webportal.app.models.DiscussionModel import DiscussionTopicTable
from webportal.lib.ModelHelpers import make_created_user, make_created_datetime


@make_created_user()
@make_created_datetime()
class BugTable(models.Model):
    StatusChoice = (
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
    )

    RelatedBug = models.ForeignKey("self")
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    ReproduceSteps = models.TextField()
    Version = models.CharField(max_length=255)
    Status = models.CharField(choices=StatusChoice)
    TimeStamp = models.DateTimeField()


class BugDiscussionTable(models.Model):
    Bug = models.ForeignKey(BugTable)
    DiscussionTopic = models.ForeignKey(DiscussionTopicTable)


class BugAttachmentTable(models.Model):
    Bug = models.ForeignKey(BugTable)
    Attachment = models.ForeignKey(AttachmentTable)


class BugTaskTable(models.Model):
    Bug = models.ForeignKey(BugTable)
    Task = models.ForeignKey(TaskTable)
