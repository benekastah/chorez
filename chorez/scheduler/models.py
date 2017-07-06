from django.db import models
from django.contrib.postgres.fields import ArrayField


class Person(models.Model):

    name = models.TextField()


class Chore(models.Model):

    name = models.TextField()
    duration = models.DurationField()
    frequency = models.PositiveSmallIntegerField(default=1)
    days = ArrayField(models.PositiveSmallIntegerField(), default=list)
    blocked_by = models.ManyToManyField('self')


class Schedule(models.Model):

    date = models.DateField()
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    owner = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
