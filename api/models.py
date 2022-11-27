from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AuditModel(models.Model):
    """ Base Model for all models, providing insertion and updating timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BlackListedToken(AuditModel):
    token = models.TextField()

    def __str__(self):
        return self.token


class Todolist(AuditModel):
    user= models.ForeignKey(User, related_name="todo_user", on_delete=models.CASCADE,
                                   default=None, null=True)
    name=models.CharField(max_length=254, blank=True)

class Tasks(AuditModel):
    todo = models.ForeignKey(Todolist, related_name="todo_task", on_delete=models.CASCADE,
                                   default=None, null=True)
    priority=models.IntegerField(null=True, default=0)
    name=models.CharField(max_length=254, blank=True)
    status=models.CharField(max_length=254, blank=True)
    active=models.BooleanField(default=False)