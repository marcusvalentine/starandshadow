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
        return self.file.name


    def _get_thumbnail(self, *args, **kwargs):
        try:
            return get_thumbnail(*args, **kwargs)
        except (IOError, IndexError, TypeError):
            i = Picture.objects.get(id=2072)
            self.file = i.file
            return get_thumbnail(self, "400")

    def _get_file(self):
        try:
            w = self.file.width
            return self.file
        except (IOError, IndexError, TypeError):
            i = Picture.objects.get(id=2072)
            self.file = i.file
            return self.file

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
        f = self._get_file()
        return f.width

    @property
    def height(self):
        f = self._get_file()
        return f.height

    @property
    def thumbnailSrc(self):
        if self._thumbnail is None:
            self._thumbnail = self._get_thumbnail(self, '100x100', crop='top')
        return self._thumbnail.url

    @property
    def thumbnailHeight(self):
        if self._thumbnail is None:
            self._thumbnail = self._get_thumbnail(self, '100x100', crop='top')
        return self._thumbnail.height

    @property
    def thumbnailWidth(self):
        if self._thumbnail is None:
            self._thumbnail = self._get_thumbnail(self, '100x100', crop='top')
        return self._thumbnail.width

    @property
    def displaySrc(self):
        if self._display is None:
            self._display = self._get_thumbnail(self, "400")
        return self._display.url

    @property
    def displayHeight(self):
        if self._display is None:
            self._display = self._get_thumbnail(self, "400")
        return self._display.height

    @property
    def displayWidth(self):
        if self._display is None:
            self._display = self._get_thumbnail(self, "400")
        return self._display.width

    def save(self, *args, **kwargs):
        self.slug = self.file.name.split('/')[-1]
        self.modified = date.today()
        super(Picture, self).save(*args, **kwargs)


class PictureAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Picture, PictureAdmin)

