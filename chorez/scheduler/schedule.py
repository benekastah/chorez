from collections import defaultdict
import datetime

from chorez.scheduler.models import Chore, Person


def get_minutes(td):
    return td.seconds // 60


def is_weekend(date):
    return date.isoweekday() in (6, 7)


def is_right_day(day, chore):
    return is_weekend(day) or not chore.weekends_only


def get_schedule(num_days=14):
    today = datetime.datetime.today().date()
    people = Person.objects.all()
    dates = tuple(today + datetime.timedelta(days=i) for i in range(num_days))
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
            elif (is_right_day(due_by, chore) and
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
