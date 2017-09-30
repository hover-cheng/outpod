from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    userpermission = models.CharField(max_length=100, null=True, blank=True)
    belong_to = models.OneToOneField(to=User, related_name='userprofile')

    def __str__(self):
        return self.name


class ProjectList(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GroupList(models.Model):
    name = models.CharField(max_length=50)
    belong_to = models.ForeignKey(to=ProjectList, related_name='project', null=True)

    def __str__(self):
        return self.name


class ServerList(models.Model):
    ip = models.GenericIPAddressField()
    description = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=10, null=True, blank=True)
    belong_to = models.ForeignKey(to=GroupList, related_name='group')

    def __str__(self):
        return self.ip


class CommandList(models.Model):
    name = models.CharField(max_length=20)
    command = models.TextField()

    def __str__(self):
        return self.name


class OperationLog(models.Model):
    ip = models.GenericIPAddressField()
    operation = models.CharField(max_length=100)
    operator = models.CharField(max_length=30)
    createtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip


class AppName(models.Model):
    appname = models.CharField(max_length=50)

    def __str__(self):
        return self.appname


class MvnType(models.Model):
    typename = models.CharField(max_length=10)

    def __str__(self):
        return self.typename


class MvnOrder(models.Model):
    mvnorder = models.CharField(max_length=50)

    def __str__(self):
        return self.mvnorder
