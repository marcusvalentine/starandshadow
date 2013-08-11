from django.db import models
from datetime import time
from django.utils import timezone
from django.conf import settings
import pytz

tz = pytz.timezone(settings.TIME_ZONE)
timezone.activate(tz)

DOC_TYPE = (('Film Review', 'Film Review'), ('Art Review', 'Art Review'), ('Book Review', 'Book Review'), ('Music Review', 'Music Review'), ('Essay', 'Essay'), ('General', 'General'),)


class Menu(models.Model):
    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=50)
    linkText = models.SlugField()

    def asLi(self):
        pages = Page.objects.filter(parent=self)
        if len(pages) > 0:
            return '\n\t'.join([page.asLi() for page in pages])
        return ''

    def asUl(self):
        li = self.asLi()
        if len(li) > 0:
            return '<ul class="side-nav">\n\t%s\n</ul>' % li
        return ''

    def asSmod(self):
        return '''<div class="mod smod">
    <div class="bd">
        %s
    </div>
</div>''' % self.asUl()

    @property
    def api_list_url(self):
        return '/api/select/menu/'


class Page(models.Model):
    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=150)
    linkText = models.SlugField()
    parent = models.ForeignKey(Menu)
    order = models.IntegerField()
    body = models.TextField(blank=True, )

    def relativeUrl(self):
        return '/' + self.linkText

    def prettyLink(self):
        return '<a href="%s">%s</a>' % (self.relativeUrl(), self.title)

    def asLi(self, extraContent=''):
        return '<li>%s%s</li>' % (self.prettyLink(), extraContent)

    @property
    def api_list_url(self):
        return '/api/select/page/'


class News(models.Model):
    class Meta:
        ordering = ['-publishDate']
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=150)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True, )
    graphic = models.ImageField(blank=True, upload_to='img/content')
    caption = models.CharField(blank=True, max_length=300)
    publishDate = models.DateTimeField()
    withdrawDate = models.DateTimeField()

    def current(self):
        now = timezone.datetime.now()
        return (now > self.publishDate) and (now < self.withdrawDate)

    current.boolean = True


class Document(models.Model):
    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=200)
    source = models.CharField(blank=True, max_length=150)
    summary = models.TextField(blank=True)
    author = models.CharField(blank=True, max_length=150)
    created = models.DateField()
    type = models.CharField(max_length=15, choices=DOC_TYPE, default="General")
    body = models.TextField(blank=True, )

    @models.permalink
    def get_absolute_url(self):
        return ('ss.content.views.documentView', (), {'id': self.id, })

    @models.permalink
    def get_edit_url(self):
        return ('ss.content.views.documentEdit', (), {'id': self.id, })

    @property
    def createdDatetime(self):
        return timezone.make_aware(timezone.datetime.combine(self.created, time(0, 0)), tz)

    @property
    def api_url(self):
        return '/api/document/'