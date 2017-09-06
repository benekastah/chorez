from collections import defaultdict
import datetime

import pytz
from django.db.models import F, DateField
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic

from chorez.scheduler.models import Chore, Person
from chorez.scheduler.forms import ChoreForm, ChoreMarkDoneForm


class ChoreList(generic.ListView):
    template_name = 'chore_list.html'

    def get_queryset(self):
        return Chore.objects.all().order_by('last_done')


class ChoreCreate(generic.CreateView):

    template_name = 'chore_create.html'
    form_class = ChoreForm
    success_url = reverse_lazy('chores')


class ChoreEdit(generic.UpdateView):

    template_name = 'chore_edit.html'
    model = Chore
    form_class = ChoreForm
    success_url = reverse_lazy('chores')


class ChoreDelete(generic.DeleteView):

    template_name = 'chore_delete.html'
    model = Chore
    success_url = reverse_lazy('chores')


class ChoreMarkDone(generic.UpdateView):

    template_name = '_chore_mark_done.html'
    model = Chore
    form_class = ChoreMarkDoneForm

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse('home')


def get_minutes(td):
    return td.seconds // 60


def is_weekend(date):
    return date.isoweekday() in (6, 7)


class ScheduleView(generic.TemplateView):
    template_name = 'schedule.html'

    def is_right_day(self, day, chore):
        return is_weekend(day) or not chore.weekends_only

    def available(self, availability, chore):
        pass

    def get_schedule(self):
        today = datetime.datetime.today().date()
        people = Person.objects.all()
        dates = tuple(today + datetime.timedelta(days=i) for i in range(14))
        availability = defaultdict(int)
        for person in people:
            for date in dates:
                if is_weekend(date):
                    availability[date] += get_minutes(person.weekend_availability)
                else:
                    availability[date] += get_minutes(person.weekday_availability)

        print('availability: %r' % availability)

        chores = Chore.objects.order_by('last_done')
        chores_by_day = defaultdict(list)
        for chore in chores:
            due_by = chore.last_done
            while due_by <= dates[-1]:
                if due_by < today:
                    due_by = max(due_by + chore.frequency, today)
                elif (self.is_right_day(due_by, chore) and
                        availability[due_by] >= get_minutes(chore.duration)):
                    chores_by_day[due_by].append(chore)
                    availability[due_by] -= get_minutes(chore.duration)
                    due_by += chore.frequency
                else:
                    due_by += datetime.timedelta(days=1)

        schedule = []
        for date in dates:
            schedule.append({
                'date': date.strftime('%a, %b %-d'),
                'chores': [
                    {'name': c.name, 'minutes': get_minutes(c.duration), 'id': c.id}
                    for c in chores_by_day[date]
                ]
            })

        return schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = self.get_schedule()
        return context
