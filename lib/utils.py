from dateutil.relativedelta import *
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import reversion
from content.models import Page, Document
from programming.models import Season, Film, Gig, Event, Festival, Meeting
from organisation.models import LogItem, Approval
from django.core.exceptions import FieldError
from django.conf import settings
import pytz
import itertools
from lib.middleware import CurrentUser
from datetime import date

tz = pytz.timezone(settings.TIME_ZONE)
utc = pytz.timezone("UTC")
timezone.activate(tz)


class Prog(object):
    def __init__(self, **kwargs):
        if 'types' in kwargs:
            self.results = kwargs['types']
        else:
            if 'all' in kwargs and kwargs['all'] is True:
                self.results = [Season.objects, Film.objects, Gig.objects, Event.objects, Festival.objects,
                                Meeting.objects]
            else:
                self.results = [Film.objects, Gig.objects, Event.objects, Festival.objects, Meeting.objects]
        self.results = [r.filter(deleted=False) for r in self.results]
        self.filter(**kwargs)
        if 'cal' in kwargs:
            self.cal = kwargs['cal']
        else:
            self.cal = None

    def calFilter(self, r, cal):
        return r.filter(startDate__gte=cal.startDate(), startDate__lte=cal.endDate())

    def startDateFilter(self, r, startDate):
        return r.filter(startDate__gte=startDate)

    def endDateFilter(self, r, endDate):
        return r.filter(startDate__lte=endDate)

    def volunteerFilter(self, r, volunteer):
        return r.filter(programmer=volunteer)

    def festivalFilter(self, r, festival):
        try:
            return r.filter(festival=festival)
        except FieldError:
            return r.filter(title='this will never return a result')

    def seasonFilter(self, r, season):
        try:
            return r.filter(season=season)
        except FieldError:
            return r.filter(title='this will never return a result')

    def approvedFilter(self, r, approved):
        try:
            return [x for x in r if x.approved]
        except TypeError:
            return [x for x in r.all() if x.approved]
        except FieldError:
            return r

    def publicFilter(self, r, public):
        try:
            return r.filter(private=False)
        except FieldError:
            return r

    def featuredFilter(self, r, featured):
        if featured:
            try:
                return r.filter(featured=True)
            except FieldError:
                return r.filter(title='this will never return a result')
        return r

    def filter(self, **kwargs):
        for filter in ['cal', 'startDate', 'endDate', 'volunteer', 'festival', 'season', 'featured', 'public',
                       'approved']:
            try:
                self.results = [getattr(self, filter + 'Filter')(r, kwargs[filter]) for r in self.results]
            except KeyError:
                pass

    def byDate(self, cal=None, trimmed=False, reverse=False):
        prog = self.flat()
        if cal is None:
            cal = self.cal
        if cal is None:
            days = sorted(list(set([item.startDate for item in prog])))
            if reverse:
                days.reverse()
        else:
            days = cal.days()
        result = [[x, sorted([item for item in prog if item.startDate == x], key=lambda y: y.startDateTime)] for x in
                  days]
        if trimmed:
            result = [x for x in result if len(x[1]) > 0]
        return result

    def flat(self):
        return [x for x in itertools.chain(*self.list())]

    def list(self):
        return self.results


@receiver(post_save, sender=Season)
@receiver(post_save, sender=Film)
@receiver(post_save, sender=Gig)
@receiver(post_save, sender=Event)
@receiver(post_save, sender=Festival)
@receiver(post_save, sender=Meeting)
def programmeChanged(sender, **kwargs):
    event = kwargs['instance']
    #print kwargs['update_fields'] TODO: When Django 1.5 is released we can make use of this to distinguish between approvals and other changes.
    if kwargs['created']:
        changetype = 'added'
    else:
        changetype = 'modified'
    editing_user = CurrentUser().programmer
    if editing_user is None:
        l = LogItem(logtext='%s %s by unknown: %s %s' % (
        event.typeName, changetype, event.get_link, event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
    else:
        l = LogItem(logtext='%s %s by %s: %s %s' % (event.typeName, changetype, editing_user.get_link, event.get_link,
                                                    event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
    l.save()


@receiver(post_save, sender=Approval)
def eventApproved(sender, **kwargs):
    approval = kwargs['instance']
    if not kwargs['created']:
        try:
            event = approval.event
            editing_user = CurrentUser().programmer
            if editing_user is None:
                l = LogItem(logtext='%s approved by unknown: %s %s' % (
                event.typeName, event.get_link, event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
            else:
                l = LogItem(logtext='%s approved by %s: %s %s' % (
                event.typeName, editing_user.get_link, event.get_link, event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
            l.save()
            message = '''A %s has been APPROVED on the website by %s:

%s
%s
http://www.starandshadow.org.uk%s
''' % (
                event.typeName,
                editing_user.name,
                event.listHeading,
                event.startDateTime.strftime('%Y/%m/%d, %H:%M'),
                event.get_absolute_url(),
            )
            send_mail(
                'S&S Website Change: %s, %s approved added by %s' % (
                event.startDateTime.strftime('%Y/%m/%d, %H:%M'), event.title, editing_user.name),
                message,
                'info@starandshadow.org.uk',
                [settings.NOTIFICATIONS_RECIPIENT, ],
                fail_silently=False,
            )
        except IndexError:
            pass


@receiver(pre_delete, sender=Approval)
def eventUnapproved(sender, **kwargs):
    approval = kwargs['instance']
    try:
        event = approval.event
        editing_user = CurrentUser().programmer
        if editing_user is None:
            l = LogItem(logtext='%s unapproved by unknown: %s %s' % (
            event.typeName, event.get_link, event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
        else:
            l = LogItem(logtext='%s unapproved by %s: %s %s' % (
            event.typeName, editing_user.get_link, event.get_link, event.startDateTime.strftime('%Y/%m/%d, %H:%M')))
        l.save()
        message = '''A %s has been UNAPPROVED on the website by %s:

%s
%s
http://www.starandshadow.org.uk%s
''' % (
            event.typeName,
            editing_user.name,
            event.listHeading,
            event.startDateTime.strftime('%Y/%m/%d, %H:%M'),
            event.get_absolute_url(),
        )
        send_mail(
            'S&S Website Change: %s, %s approval deleted by %s' % (
            event.startDateTime.strftime('%Y/%m/%d, %H:%M'), event.title, editing_user.name),
            message,
            'info@starandshadow.org.uk',
            [settings.NOTIFICATIONS_RECIPIENT, ],
            fail_silently=False,
        )
    except IndexError:
        pass


@receiver(post_save, sender=Page)
@receiver(post_save, sender=Document)
def contentChanged(sender, **kwargs):
    item = kwargs['instance']
    if kwargs['created']:
        changetype = 'added'
    else:
        changetype = 'modified'
    editing_user = CurrentUser().programmer
    if editing_user is None:
        editing_user = 'unknown'
    l = LogItem(logtext='%s "%s" %s by %s.' % (item._meta.object_name, item.prettyLink(), changetype, editing_user))
    l.save()
    message = '''%s "%s" has been %s on the website by %s.
''' % (
        item._meta.object_name,
        item,
        changetype,
        editing_user,
    )
    send_mail('Website Change: "%s", %s' % (item, changetype, ),
              message,
              'info@starandshadow.org.uk',
              [settings.NOTIFICATIONS_RECIPIENT, ],
              fail_silently=False,
    )


class ssDate(object):
    def __init__(self, dateObj=None, **kwargs):
        self.now = timezone.now().astimezone(tz)
        size = 'month'
        if dateObj is None:
            if 'year' in kwargs and kwargs['year'] is not None:
                year = int(kwargs['year'])
                if year > self.now.year + 20:
                    year = self.now.year + 20
                elif year < self.now.year - 20:
                    year = self.now.year - 20
                size = 'year'
            else:
                year = self.now.year
            if 'week' in kwargs and kwargs['week'] is not None:
                week = int(kwargs['week'])
                self.date = date(year, 1, 1) + relativedelta(day=1, weekday=MO(-1), weeks=week)
                size = 'week'
            else:
                if 'month' in kwargs and kwargs['month'] is not None:
                    month = int(kwargs['month'])
                    size = 'month'
                else:
                    month = self.now.month
                if 'day' in kwargs and kwargs['day'] is not None:
                    day = int(kwargs['day'])
                    size = 'day'
                else:
                    day = self.now.day
                try:
                    self.date = date(year, month, day)
                except ValueError:
                    self.date = date(year, month, 1) + relativedelta(months=1) - relativedelta(days=1)
        else:
            self.date = dateObj
        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = size

    def yesterday(self):
        return self.date - relativedelta(days=1)

    def tomorrow(self):
        return self.date + relativedelta(days=1)

    def sameDayLastWeek(self):
        return self.date - relativedelta(weeks=1)

    def sameDayNextWeek(self):
        return self.date + relativedelta(weeks=1)

    def sameDayLastMonth(self):
        return self.date - relativedelta(months=1)

    def sameDayNextMonth(self):
        return self.date + relativedelta(months=1)

    def sameDayLastYear(self):
        return self.date - relativedelta(years=1)

    def sameDayNextYear(self):
        return self.date + relativedelta(years=1)

    def startOfYear(self):
        return self.date.replace(month=1, day=1)

    def endOfYear(self):
        return self.startOfYear() + relativedelta(years=1, days=-1)

    def startOfMonth(self):
        return self.date.replace(day=1)

    def endOfMonth(self):
        return self.startOfMonth() + relativedelta(months=1, days=-1)

    def startOfWeek(self):
        return self.date - relativedelta(weekday=MO(-1))

    def endOfWeek(self):
        return self.date + relativedelta(weekday=SU)

    def previousMonth(self):
        return self.sameDayLastMonth()

    def nextMonth(self):
        return self.sameDayNextMonth()

    def days(self):
        days = []
        d = self.startDate()
        end = self.endDate()
        while d <= end:
            days.append(d)
            d = d + relativedelta(days=1)
        return days

    def startDate(self):
        if self.size == 'year':
            return self.startOfYear()
        elif self.size == 'month':
            return self.startOfMonth()
        elif self.size == 'week':
            return self.startOfWeek()
        elif self.size == 'day':
            return self.date
        raise Exception

    def endDate(self):
        if self.size == 'year':
            return self.endOfYear()
        elif self.size == 'month':
            return self.endOfMonth()
        elif self.size == 'week':
            return self.endOfWeek()
        elif self.size == 'day':
            return self.date
        raise Exception

    def previous(self):
        if self.size == 'year':
            return ssDate(self.sameDayLastYear(), size='year')
        elif self.size == 'month':
            return ssDate(self.sameDayLastMonth(), size='month')
        elif self.size == 'week':
            return ssDate(self.sameDayLastWeek(), size='week')
        elif self.size == 'day':
            return ssDate(self.yesterday(), size='day')
        raise Exception

    def next(self):
        if self.size == 'year':
            return ssDate(self.sameDayNextYear(), size='year')
        elif self.size == 'month':
            return ssDate(self.sameDayNextMonth(), size='month')
        elif self.size == 'week':
            return ssDate(self.sameDayNextWeek(), size='week')
        elif self.size == 'day':
            return ssDate(self.tomorrow(), size='day')
        raise Exception

    def url(self):
        if self.size == 'year':
            return self.date.strftime('%Y/')
        elif self.size == 'month':
            return self.date.strftime('%Y/%m/')
        elif self.size == 'week':
            return self.date.strftime('%Y/w%U/')
        elif self.size == 'day':
            return self.date.strftime('%Y/%m/%d/')
        raise Exception

    def onUrl(self):
        return '/on/' + self.url()

    def orgUrl(self):
        return '/org' + self.onUrl()

    def __unicode__(self):
        if self.size == 'year':
            return self.date.strftime('%Y')
        elif self.size == 'month':
            return self.date.strftime('%B %Y')
        elif self.size == 'week':
            if self.startDate().year == self.endDate().year:
                return self.startDate().strftime('%A %d %b') + ' to ' + self.endDate().strftime('%A %d %b %Y')
            else:
                return self.startDate().strftime('%A %d %b %Y') + ' to ' + self.endDate().strftime('%A %d %b %Y')
        elif self.size == 'day':
            return self.date.strftime('%A %d %b %Y')
        raise Exception

    def strftime(self, *args, **kwargs):
        return self.date.strftime(*args, **kwargs)

