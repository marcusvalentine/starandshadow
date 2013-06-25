from django.db import models

class Minutes(models.Model):
    meeting     = models.ForeignKey('programming.Meeting')
    body        = models.TextField(blank=True,)
    file        = models.FileField(blank=True,upload_to='doc/minutes')
    @models.permalink
    def get_absolute_url(self):
        return 'ss.organisation.views.minutesView', (), {'id': self.id,}
    @models.permalink
    def get_edit_url(self):
        return 'ss.organisation.views.minutesEdit', (), {'id': self.id,}
    def __unicode__(self):
        try:
            return "Minutes of %s" % self.meeting.longHeading
        except AttributeError:
            return "Minutes of unspecified meeting"
    @property
    def listHeading(self):
        return self.__unicode__()
    @property
    def api_url(self):
        return '/api/minutes/'

class PrintProgramme(models.Model):
    embedcode = models.TextField(blank=True,)
    pdffile = models.FileField(blank=True,upload_to='doc/programme')
    start = models.DateField()
    end = models.DateField()

class ApprovalSet(models.Model):
    meeting     = models.OneToOneField('programming.Meeting')
    def __unicode__(self):
        return '%s, %s, %s' % (self.id, self.meeting.id, self.meeting)
    @property
    def approvals(self):
        apps = [x for x in self.approval_set.all()]
        apps.sort(key=lambda x: x.event.startDateTime)
        return apps

class Approval(models.Model):
    approvalset = models.ForeignKey('ApprovalSet')
    approver = models.ForeignKey('programming.Programmer')
    @property
    def event(self):
        for itemset in ['season_set', 'film_set', 'gig_set', 'event_set', 'festival_set', 'meeting_set']:
            related = self.__getattribute__(itemset).all()
            if len(related) == 1:
                return related[0]
        return None
    @property
    def itemapprovalinfo(self):
        event = self.event
        meeting = self.approvalset.meeting
        return 'This %s was approved at the <a href="%s">%s</a> on %s by <a href="%s">%s</a>' % (
            event.typeName,
            meeting.get_absolute_url(),
            meeting.listHeading,
            meeting.displayStartEndShort,
            self.approver.get_absolute_url(),
            self.approver
        )
    def __unicode__(self):
        event = self.event
        return '%s: <a href="%s">%s</a> approved by <a href="%s">%s</a>' % (event.typeName, event.get_absolute_url(), event.title, self.approver.get_absolute_url(), self.approver)

class BoxOfficeReturn(models.Model):
    film = models.ForeignKey('programming.Film')
    newMembers = models.IntegerField(default=0, blank=False)
    membershipPrice = models.DecimalField(default=1.00, max_digits=5, decimal_places=2, blank=False)
    normalTickets = models.IntegerField(default=0, blank=False)
    normalPrice = models.DecimalField(default=5.00, max_digits=5, decimal_places=2, blank=False)
    concessionTickets = models.IntegerField(default=0, blank=False)
    concesionPrice = models.DecimalField(default=3.50, max_digits=5, decimal_places=2, blank=False)
    def membershipTake(self):
        return self.newMembers * self.membershipPrice
    def normalTake(self):
        return self.normalTickets * self.normalPrice
    def concessionTake(self):
        return self.concessionTickets * self.concesionPrice
    def ticketTake(self):
        return self.normalTake() + self.concessionTake()
    def totalTake(self):
        return self.normalTake() + self.concessionTake() + self.membershipTake()
    def membership(self):
        return '%s @ &pound;%s = &pound;%s' % (self.newMembers, self.membershipPrice, self.membershipTake())
    def normal(self):
        return '%s @ &pound;%s = &pound;%s' % (self.normalTickets, self.normalPrice, self.normalTake())
    def concession(self):
        return '%s @ &pound;%s = &pound;%s' % (self.concessionTickets, self.concesionPrice, self.concessionTake())
    def ticket(self):
        return '&pound;%s' % self.ticketTake()
    def __unicode__(self):
        return 'Returns for %s %s' % (self.film.title, self.film.displayTime)

class LogItem(models.Model):
    logdate = models.DateTimeField(auto_now_add=True)
    logtext = models.CharField(max_length=1000)
    class Meta:
        ordering = ['-logdate']