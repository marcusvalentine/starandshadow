from django.db import models
from django.contrib import admin
from datetime import date
from sorl.thumbnail import get_thumbnail


class Picture(models.Model):
    file = models.ImageField(upload_to="img/events")
    slug = models.SlugField(max_length=200, blank=True)
    modified = models.DateField()
    _thumbnail = None
    _display = None

    def __unicode__(self):
        try:
            return self.file.name
        except (IOError, IndexError):
            return 100


    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    @property
    def get_img_url(self):
        return '/static/%s' % self.file.name

    @property
    def api_model_url(self):
        return '/api/1/picture/'

    @property
    def api_object_url(self):
        if self.id is None:
            return '/api/1/picture/'
        else:
            return '/api/1/picture/%s/' % self.id

    @property
    def api_list_model_url(self):
        return '/api/1/selectpicture/'

    @property
    def src(self):
        return self.get_img_url

    @property
    def width(self):
        try:
            return self.file.width
        except (IOError, IndexError):
            return 100

    @property
    def height(self):
        try:
            return self.file.height
        except (IOError, IndexError):
            return 100

    @property
    def thumbnailSrc(self):
        try:
            if self._thumbnail is None:
                self._thumbnail = get_thumbnail(self, '100x100', crop='top')
            return self._thumbnail.url
        except (IOError, IndexError):
            return ''

    @property
    def thumbnailHeight(self):
        try:
            if self._thumbnail is None:
                    self._thumbnail = get_thumbnail(self, '100x100', crop='top')
            return self._thumbnail.height
        except (IOError, IndexError):
            return 100

    @property
    def thumbnailWidth(self):
        try:
            if self._thumbnail is None:
                self._thumbnail = get_thumbnail(self, '100x100', crop='top')
            return self._thumbnail.width
        except (IOError, IndexError):
            return 100

    @property
    def displaySrc(self):
        try:
            if self._display is None:
                self._display = get_thumbnail(self, "400")
            return self._display.url
        except (IOError, IndexError):
            return 400

    @property
    def displayHeight(self):
        try:
            if self._display is None:
                self._display = get_thumbnail(self, "400")
            return self._display.height
        except (IOError, IndexError):
            return 400

    @property
    def displayWidth(self):
        try:
            if self._display is None:
                self._display = get_thumbnail(self, "400")
            return self._display.width
        except (IOError, IndexError):
            return 400

    def save(self, *args, **kwargs):
        self.slug = self.file.name.split('/')[-1]
        self.modified = date.today()
        super(Picture, self).save(*args, **kwargs)


class PictureAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Picture, PictureAdmin)

