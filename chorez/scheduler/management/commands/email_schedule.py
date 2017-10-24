import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from chorez.scheduler.schedule import get_schedule


class Command(BaseCommand):
    help = 'Sends the schedule via email'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+')

    def handle(self, *args, **options):
        print('Sending to: %r' % options['emails'])
        context = {'schedule': get_schedule(7)}
        message = render_to_string('schedule_email.txt', context=context)
        html_message = render_to_string('schedule_email.html', context=context)
        send_mail(
            subject='Chore Schedule for {}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d')),
            message=message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=options['emails'],
            fail_silently=False)
