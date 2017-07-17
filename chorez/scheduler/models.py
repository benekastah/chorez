import datetime

from django.db import models


class Person(models.Model):

    AVAILABILITY_CHOICES = (
        (datetime.timedelta(minutes=15), '15 minutes'),
        (datetime.timedelta(minutes=30), '30 minutes'),
        (datetime.timedelta(minutes=45), '45 minutes'),
        (datetime.timedelta(minutes=60), '60 minutes'),
    )

    name = models.TextField()
    weekday_availability = models.DurationField(choices=AVAILABILITY_CHOICES,
                                                default=AVAILABILITY_CHOICES[0][0])
    weekend_availability = models.DurationField(choices=AVAILABILITY_CHOICES,
                                                default=AVAILABILITY_CHOICES[0][0])

    def __str__(self):
        return self.name


def default_days():
    return list(range(7))


def default_last_done():
    return datetime.datetime.utcnow() - datetime.timedelta(days=7)


class Chore(models.Model):

    name = models.TextField()
    last_done = models.DateField(default=default_last_done, blank=True)
    snoozed_until = models.DateField(null=True, blank=True)
    duration = models.DurationField(choices=(
        (datetime.timedelta(minutes=5), '5 minutes'),
        (datetime.timedelta(minutes=10), '10 minutes'),
        (datetime.timedelta(minutes=15), '15 minutes'),
        (datetime.timedelta(minutes=30), '30 minutes'),
    ))
    frequency = models.DurationField(choices=(
        (datetime.timedelta(days=1), 'Daily'),
        (datetime.timedelta(days=2), 'Every other day'),
        (datetime.timedelta(days=3.5), 'Twice a week'),
        (datetime.timedelta(days=7), 'Weekly'),
        (datetime.timedelta(days=14), 'Every other week'),
        (datetime.timedelta(days=30), 'Monthly'),
    ))
    weekends_only = models.BooleanField(default=False, blank=True)
    blocked_by = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.name
