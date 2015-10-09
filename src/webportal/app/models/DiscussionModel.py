from django.db import models
from django.contrib.auth.models import User as AuthUser
from webportal.app.models.AttachmentModel import AttachmentTable
from webportal.lib.ModelHelpers import make_created_user, make_created_datetime


@make_created_user()
@make_created_datetime()
class DiscussionTable(models.Model):
    Parent = models.ForeignKey("self")
    Shared = models.BooleanField()
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Active = models.BooleanField()


class DiscussionUserTable(models.Model):
    Discussion = models.ForeignKey(DiscussionTable)
    User = models.ForeignKey(AuthUser)


@make_created_user()
@make_created_datetime()
class DiscussionTopicTable(models.Model):
    Discussion = models.ForeignKey(DiscussionTable)
    Name = models.CharField(max_length=255)
    Description = models.TextField()


@make_created_user()
@make_created_datetime()
class DiscussionCommentTable(models.Model):
    DiscussionTopic = models.ForeignKey(DiscussionTopicTable)
    Text = models.TextField()
    RelatedComment = models.ForeignKey("self")


class DiscussionCommentAttachmentTable(models.Model):
    DiscussionComment = models.ForeignKey(DiscussionCommentTable)
    Attachment = models.ForeignKey(AttachmentTable)

