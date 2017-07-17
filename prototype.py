from enum import Enum, auto
from collections import defaultdict


def indented(level, txt):
    lines = txt.splitlines()
    indent = ''.join(' ' for _ in range(level))
    for line in lines:
        yield '{}{}'.format(indent, line)


def joinlines(fn):
    def wrapper(*args, **kwargs):
        return '\n'.join(fn(*args, **kwargs))
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


class Days(Enum):
    SUNDAY = 'Sunday'
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'

    @classmethod
    def as_list(cls):
        return [cls.SUNDAY, cls.MONDAY, cls.TUESDAY, cls.WEDNESDAY, cls.THURSDAY, cls.FRIDAY, cls.SATURDAY]

    @classmethod
    def everyday(cls):
        return set(cls.as_list())

    @classmethod
    def weekends(cls):
        return {cls.SUNDAY, cls.SATURDAY}

    @classmethod
    def weekdays(cls):
        return cls.everyday() - cls.weekends()


class Person:

    def __init__(self, name, weekday_effort, weekend_effort):
        self.name = name
        self.effort_per_day = {}
        for day in Days.everyday():
            if day in Days.weekends():
                self.effort_per_day[day] = weekend_effort
            else:
                self.effort_per_day[day] = weekday_effort

    def __str__(self):
        return self.name


class People(Enum):
    MOM = Person('Mom', 30, 45)
    DAD = Person('Dad', 15, 45)
    EMI = Person('Emi', 15, 45)

    @classmethod
    def everyone(cls):
        return {cls.MOM, cls.DAD, cls.EMI}

    @classmethod
    def parents(cls):
        return {cls.MOM, cls.DAD}

    @classmethod
    def Emi(cls):
        return {cls.EMI}


class Chore:

    def __init__(self, name, effort, per_week=7, when=None):
        self.name = name
        self.effort = effort
        self.per_week = per_week
        self.when = when or Days.everyday()

    def __str__(self):
        return '({}m) {}'.format(self.effort, self.name)


class ChoreGroup(Chore):

    def __init__(self, name, per_week, chores, when=None):
        effort = sum(c.effort for c in chores)
        super().__init__(name, effort, per_week, when=when)
        for chore in chores:
            chore.per_week = self.per_week
            chore.when = self.when
        self.chores = chores

    @joinlines
    def __str__(self):
        yield self.name
        yield from indented(2, '\n'.join(str(c) for c in self.chores))


class DoesNotFit(Exception):
    pass


class Week:

    def __init__(self, people):
        self.people = people
        self.effort_per_day = {}
        for d in Days.as_list():
            self.effort_per_day[d] = sum(p.value.effort_per_day[d] for p in people)
        self.chores_per_day = defaultdict(set)
        self.chore_counts = defaultdict(int)

    def schedule(self, day, chore):
        if day not in chore.when:
            raise DoesNotFit
        elif chore in self.chores_per_day[day]:
            raise DoesNotFit
        elif self.chore_counts[chore] >= chore.per_week:
            raise DoesNotFit
        elif self.effort_per_day[day] >= chore.effort:
            self.effort_per_day[day] -= chore.effort
            self.chores_per_day[day].add(chore)
            self.chore_counts[chore] += 1
        else:
            raise DoesNotFit

    @joinlines
    def __str__(self):
        for day in Days.as_list():
            yield day.value
            yield from indented(2, '\n'.join(str(c) for c in self.chores_per_day[day]))


class Schedule:

    def __init__(self, people):
        self.people = people
        self.weeks = None
        self.warnings = []

    def schedule(self, chores):
        num_weeks = int(round(max(1 / c.per_week for c in chores)))
        self.weeks = [Week(self.people) for _ in range(num_weeks)]

        chore_counts = defaultdict(int)
        for week in self.weeks:
            for chore in chores:
                for day in Days.everyday():
                    try:
                        if chore_counts[chore] >= chore.per_week * num_weeks:
                            raise DoesNotFit
                        week.schedule(day, chore)
                        chore_counts[chore] += 1
                    except DoesNotFit:
                        continue

        chore_counts_2 = defaultdict(int)
        for week in self.weeks:
            for chore in chores:
                chore_counts_2[chore] += week.chore_counts[chore]

        assert chore_counts == chore_counts_2

        for chore in chores:
            count = chore_counts[chore]
            per_week = count / num_weeks
            if per_week != chore.per_week:
                self.warnings.append(
                    '{} needs to be done {} times per week, but was '
                    'scheduled {} times per week'.format(chore, chore.per_week, per_week))

    @joinlines
    def __str__(self):
        yield from self.warnings
        if self.warnings:
            yield ''
        for i, week in enumerate(self.weeks):
            yield 'Week {}'.format(i + 1)
            yield from indented(2, str(week))
            yield ''


# Chores, in order of priority
CHORES = [
    ChoreGroup('Laundry', 1, [
        Chore('Run laundry', 15),
        Chore('Hang up laundry', 15),
        Chore('Fold laundry', 30)
    ], when=Days.weekends()),
    Chore('Clean up messes (Emi)', 5, 7),
    Chore('Empty/load dishwasher', 10, 7),
    ChoreGroup('Sweep and mop', .5, [
        Chore('Sweep floors', 15),
        Chore('Mop floors', 15)
    ]),
    Chore('Kitchen table and counters', 10, 7),
    Chore('Pans', 10, 7),
    Chore('Straighten bedroom (Emi)', 5, 7),
    Chore('Straighten living room', 5, 7),
    Chore('Straighten bedroom (parent)', 5, 7),
    Chore('Take out the trash', 5, 1),
    Chore('Pippin\'s poop', 5, 1),
    Chore('Vacuum bedrooms', 15, 1),
    Chore('Vacuum living room', 15, 1),
    Chore('Clean shower', 5, .5),
    Chore('Bathroom sink', 15, 1),
    Chore('Clean toilet', 15, 1),
    Chore('Dusting', 5, 1),
    Chore('Clean the windows', 5, .5),
]


def schedule_chores():
    schedule = Schedule(People.everyone())
    schedule.schedule(CHORES)
    print(str(schedule))


if __name__ == '__main__':
    schedule_chores()
