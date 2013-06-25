from django.db import models
from django.contrib.auth.models import User
from ss.fileupload.models import Picture
import re
import htmlentitydefs
import pytz
from django.template.defaultfilters import date as django_date_filter
from django.utils import timezone
from datetime import time
from django.conf import settings

FILM_FORMATS = (("Unknown", "Unknown"), ("16mm", "16mm"), ("35mm", "35mm"), ("DVD", "DVD"), ("VHS", "VHS"), ("DigiBeta", "DigiBeta"), ("Various", "Various"), ("Other", "Other"))
MEETING_TYPES = (
    ('General Meeting', 'General Meeting'),
    ('Programming Meeting', 'Programming Meeting'),
    ('Bar Meeting', 'Bar Meeting'),
    ('Publicity Meeting', 'Publicity Meeting'),
    ('AGM', 'AGM'),
    ('Other Meeting', 'Other Meeting'),
)
whitespace = re.compile('\n\s*\n', re.MULTILINE)
twhitespace = re.compile('\s*$', re.MULTILINE)
tz = pytz.timezone(settings.TIME_ZONE)
utc = pytz.timezone("UTC")
timezone.activate(tz)


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


class ProgrammeType(object):
    approval = None
    _meta = None
    title = None
    confirmed = False

    @property
    def approved(self):
        return self.approval is not None

    @property
    def valid(self):
        return True

    @property
    def typeName(self):
        return self._meta.object_name

    @property
    def api_model_url(self):
        return '/api/1/%s/' % self.typeName.lower()

    @property
    def api_object_url(self):
        if self.id is None:
            return '/api/1/%s/' % self.typeName.lower()
        else:
            return '/api/1/%s/%s/' % (self.typeName.lower(), self.id)

    @property
    def api_list_url(self):
        return '/api/1/select%s/' % self.typeName.lower()

    @property
    def get_link(self):
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), self.title)

    def get_absolute_url(self):
        raise NotImplementedError("Please Implement this method.")

    # noinspection PyUnusedLocal
    def extramessage(self, request):
        extramessages = []
        if self.confirmed:
            extramessages.append('<div class="message info">This is a confirmed booking.  This means it is no longer a provisional booking.<button class="unconfirmitem" href="#">Unconfirm</button></div>')
        else:
            extramessages.append('<div class="message warning">This is a provisional booking.<button class="confirmitem" href="#">Confirm</button></div>')
        if self.approved:
            extramessages.append('<div class="message info">%s<button class="unapproveitem" href="#">Unapprove</button><div id="approvedialog" hidden></div></div>' % self.approval.itemapprovalinfo)
        else:
            extramessages.append('<div class="message warning">This %s is not approved.<button class="approvedialog" href="#">Approve</button><div id="approvedialog" hidden></div></div>' % self.typeName)
        return extramessages

    @property
    def validityMessages(self):
        if self.valid:
            return ["Details are valid.", ]
        else:
            return ["Details are not valid.", ]

class EventType(object):
    class Meta:
        ordering = ['startDate', 'startTime']

    def __unicode__(self):
        return self.title

    @property
    def typeName(self):
        return self._meta.object_name

    @property
    def listHeading(self):
        if self.private:
            return 'Private Booking'
        else:
            return self.title
            #return self.typeName + ': ' + self.title

    def plainText(self, formatString=None):
        if formatString is None:
            formatString = '''%(typeName)s
%(title)s
%(day)s
%(start)s to %(end)s
%(summary)s
'''
        if self.private:
            formatString = 'PRIVATE ' + formatString
        if not self.approved:
            formatString = 'UNAPPROVED ' + formatString
        return formatString % {
            'typeName': self._meta.object_name.upper(),
            'title': self.title,
            'day': self.start.strftime('%A %d'),
            'start': self.start.strftime('%H:%M'),
            'end': self.end.strftime('%H:%M'),
            'summary': unescape(twhitespace.sub('', whitespace.sub('\n', self.summary))),
        }

    @property
    def startDateTime(self):
        return timezone.make_aware(timezone.datetime.combine(self.startDate, self.startTime), tz)

    @property
    def endDateTime(self):
        return timezone.make_aware(timezone.datetime.combine(self.endDate, self.endTime), tz)

    def __getattr__(self, attr):
        if attr == 'endDate':
            if self.endTime < self.startTime:
                return self.startDate + timezone.timedelta(days=1)
            else:
                return self.startDate
        else:
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, attr))

    @property
    def displayStart(self):
        if self.endTime < self.startTime:
            if self.endDate.month == self.startDate.month:
                fmt = 'g:i a l j'
            else:
                if self.endDate.year == self.startDate.year:
                    fmt = 'g:i a l j F'
                else:
                    fmt = settings.DATETIME_FORMAT  # 'g:i a l j F Y'
        else:
            fmt = settings.TIME_FORMAT  # 'g:i a'
        return django_date_filter(self.startDateTime, fmt)

    @property
    def displayEnd(self):
        return django_date_filter(self.endDateTime, settings.DATETIME_FORMAT)

    @property
    def displayStartEnd(self):
        return '%s to %s' % (self.displayStart, self.displayEnd)


class Programmer(models.Model, ProgrammeType):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=150)
    homePhone = models.CharField(blank=True, max_length=15)
    mobilePhone = models.CharField(blank=True, max_length=15)
    email = models.EmailField(blank=True, )
    notes = models.TextField(blank=True, )
    user = models.OneToOneField(User)
    photo = models.ImageField(blank=True, upload_to='img/programmer', default='img/programmer/ron1-small.jpg')

    @models.permalink
    def get_absolute_url(self):
        return 'ss.organisation.views.volunteerProfile', (), {'id': self.user.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.volunteerEdit', (), {'id': self.user.id, }

    @property
    def get_link(self):
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), self.name)

    @property
    def valid(self):  # TODO: Do we have valid contact details for this programmer?
        return True


class Rating(models.Model, ProgrammeType):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=20)
    largeImage = models.ImageField(blank=True, upload_to='img/rating')
    smallImage = models.ImageField(blank=True, upload_to='img/rating')


class Season(models.Model, ProgrammeType, EventType):
    class Meta:
        ordering = ['startDate']

    title = models.CharField(max_length=150, default="NEW SEASON")
    startDate = models.DateField()
    endDate = models.DateField()
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True, default='<p>DEFAULT PLACEHOLDER TEXT</p>')
    picture = models.ForeignKey(Picture, blank=True, null=True)
    notes = models.TextField(blank=True, )
    programmer = models.ForeignKey(Programmer)
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.season', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.seasonEdit', (), {'id': self.id, }

    @property
    def startTime(self):
        return time(0, 0, 0)

    @property
    def endTime(self):
        return time(23, 59, 59)

    @property
    def displayStart(self):
        if self.endDate.month == self.startDate.month:
            fmt = 'l j'
        else:
            if self.endDate.year == self.startDate.year:
                fmt = 'l j F'
            else:
                fmt = settings.DATE_FORMAT  # 'l j F Y'
        return django_date_filter(self.startDate, fmt)

    @property
    def displayEnd(self):
        return django_date_filter(self.endDate, settings.DATE_FORMAT)


class Film(models.Model, ProgrammeType, EventType):
    title = models.CharField(max_length=150, default="NEW FILM")
    startDate = models.DateField()
    startTime = models.TimeField()
    length = models.CharField(blank=True, max_length=150)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True, default='<p>DEFAULT PLACEHOLDER TEXT</p>')
    director = models.CharField(blank=True, max_length=150)
    year = models.CharField(blank=True, max_length=150)
    lang = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=150)
    certificate = models.ForeignKey(Rating)
    filmFormat = models.CharField(max_length=15, choices=FILM_FORMATS, default="Unknown")
    season = models.ForeignKey(Season)
    picture = models.ForeignKey(Picture, blank=True, null=True)
    notes = models.TextField(blank=True, )
    programmer = models.ForeignKey(Programmer)
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.film', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.filmEdit', (), {'id': self.id, }

    @property
    def listHeading(self):
        if self.private:
            return 'Private Booking'
        else:
            if self.year is None or self.year == '':
                return self.title
            else:
                return '%s (%s)' % (self.title, self.year)

    def plainText(self, formatString=None):
        if formatString is None:
            formatString = '''FILM
%(title)s
%(day)s
%(start)s
Director: %(director)s
Certificate: %(certificate)s
Length: %(length)s
Language: %(lang)s
%(summary)s
'''
        if self.private:
            formatString = 'PRIVATE' + formatString
        if not self.approved:
            formatString = 'UNAPPROVED ' + formatString
        return formatString % {
            'title': self.title,
            'day': self.startDate.strftime('%A %d'),
            'start': self.startTime.strftime('%H:%M'),
            'director': self.director,
            'certificate': self.certificate,
            'length': self.length,
            'lang': self.lang,
            'summary': unescape(twhitespace.sub('', whitespace.sub('\n', self.summary))),
        }

    @property
    def endDate(self):
        return self.startDate

    @property
    def endTime(self):  # TODO: Change length to an int field and calculate this properly.  Can then also improve isolength.
        return self.startTime

    @property
    def displayStart(self):
        return django_date_filter(self.startDateTime, settings.DATETIME_FORMAT)

    @property
    def isolength(self):
        try:
            length = re.findall(r"[^\d]*(\d+)[^\d]*", self.length)[0]
        except IndexError:
            length = ''
        return 'PT%sM' % length


class Gig(models.Model, ProgrammeType, EventType):
    title = models.CharField(max_length=150, default="NEW GIG")
    startDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    summary = models.TextField(blank=True, )
    body = models.TextField(blank=True, default='<p>DEFAULT PLACEHOLDER TEXT</p>')

    website = models.URLField(blank=True, )
    picture = models.ForeignKey(Picture, blank=True, null=True)
    notes = models.TextField(blank=True, )
    programmer = models.ForeignKey(Programmer)
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.gig', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.gigEdit', (), {'id': self.id, }


class Event(models.Model, ProgrammeType, EventType):
    title = models.CharField(max_length=150, default="NEW EVENT")
    startDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    summary = models.TextField(blank=True, )
    body = models.TextField(blank=True, default='<p>DEFAULT PLACEHOLDER TEXT</p>')

    website = models.URLField(blank=True, )
    picture = models.ForeignKey(Picture, blank=True, null=True)
    notes = models.TextField(blank=True, )
    programmer = models.ForeignKey(Programmer)
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.event', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.eventEdit', (), {'id': self.id, }


class Festival(models.Model, ProgrammeType, EventType):
    title = models.CharField(max_length=150, default="NEW FESTIVAL")
    startDate = models.DateField()
    startTime = models.TimeField()
    endDate = models.DateField()
    endTime = models.TimeField()
    summary = models.TextField(blank=True, )
    body = models.TextField(blank=True, default='<p>DEFAULT PLACEHOLDER TEXT</p>')

    website = models.URLField(blank=True, )
    picture = models.ForeignKey(Picture, blank=True, null=True)
    notes = models.TextField(blank=True, )

    films = models.ManyToManyField(Film, blank=True)
    gigs = models.ManyToManyField(Gig, blank=True)
    events = models.ManyToManyField(Event, blank=True)

    notes = models.TextField(blank=True, )
    programmer = models.ForeignKey(Programmer)
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.festival', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.festivalEdit', (), {'id': self.id, }


class Meeting(models.Model, ProgrammeType, EventType):
    title = models.CharField(max_length=150, choices=MEETING_TYPES, default="General Meeting")
    startDate = models.DateField()
    startTime = models.TimeField()
    programmer = models.ForeignKey(Programmer, limit_choices_to={'id': 183})
    approval = models.ForeignKey('organisation.Approval', blank=True, null=True, on_delete=models.SET_NULL)
    private = False

    @property
    def listHeading(self):
        return self.title

    def __unicode__(self):
        return "%s %s" % (self.title, self.displayStart)

    @models.permalink
    def get_absolute_url(self):
        return 'ss.programming.views.meeting', (), {'id': self.id, }

    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.meetingEdit', (), {'id': self.id, }

    def plainText(self, formatString=None):
        if formatString is None:
            formatString = '''%(typeName)s
%(title)s
%(day)s
%(start)s
'''
        if self.private:
            formatString = 'PRIVATE ' + formatString
        if not self.approved:
            formatString = 'UNAPPROVED ' + formatString
        return formatString % {
            'typeName': self._meta.object_name.upper(),
            'title': self.title,
            'day': self.start.strftime('%A %d'),
            'start': self.start.strftime('%H:%M'),
        }

    @property
    def endDate(self):
        return self.startDate

    def endTime(self):
        return self.startTime

    @property
    def displayStart(self):
        return django_date_filter(self.startDateTime, settings.DATETIME_FORMAT)

    @property
    def confirmed(self):
        return True

    @property
    def displayStartEnd(self):
        return self.displayStart

    @property
    def displayStartEndShort(self):
        return django_date_filter(self.startDateTime, settings.SHORT_DATE_FORMAT)

    @property
    def picture(self):
        return Picture.objects.get(id=200)

    @property
    def shortDate(self):
        return django_date_filter(self.startDate, 'Y-m-d')

    @property
    def longHeading(self):
        return "%s %s" % (self.shortDate, self.listHeading)

