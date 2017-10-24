from collections import defaultdict
import datetime

import pytz
from django.db.models import F, DateField
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic

from chorez.scheduler.models import Chore, Person
from chorez.scheduler.forms import ChoreForm, ChoreMarkDoneForm
from chorez.scheduler.schedule import get_schedule


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


class ScheduleView(generic.TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = get_schedule()
        return context
