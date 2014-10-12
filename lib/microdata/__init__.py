from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe

FIELD_WIDGETS = {
    'CharField': 'span',
}


class MicroformatModel(object):
    def __init__(self, instance):
        if self.Meta.model is None:
            raise ValueError('MicroformatModel has no model class specified.')
        self._instance = instance
        #self._object_data = model_to_dict(instance, self.Meta.fields.keys())
        try:
            self._fields = self.Meta.fields
            try:
                self._widgets = self.Meta.widgets
            except AttributeError:
                self._widgets = {}
        except AttributeError:
            self._fields = {}
            self._widgets = {}

    def span(self, **kwargs):
        return '<span itemprop="%(itemprop)s" data-modelfield="%(name)s" data-fieldtype="%(fieldtype)s">%(value)s</span>' % kwargs

    def meta(self, **kwargs):
        return '<meta itemprop="%(itemprop)s" data-modelfield="%(name)s" data-fieldtype="%(fieldtype)s" content="%(value)s" />' % kwargs

    def img(self, **kwargs):
        return '''<img  data-modelfield="picture"
                        data-fieldtype="ForeignKeyPicture"
                        data-fieldvalue="{{ event.picture.id }}"
                        data-fieldapiurl="{{ event.picture.api_list_model_url }}"
                        itemprop="image"
                        src="{{ im.url }}"
                        data-src="{{ event.picture.get_img_url }}"
                        alt=""
                        width="%()s"
                        height="%()s">
                        ''' ** kwargs

    '''
<time itemprop="startDate" data-modelfield="start" data-fieldtype="DateTimeField" data-fieldvalue="{{ event.startDatetime|date:"c"|slice:":19" }}" datetime="{{ event.startDatetime|date:"c" }}">{{ event.displayStart }}</time>'''

    def __getattr__(self, name):
        value = self._instance.__getattribute__(name)
        print dir(value)
        if name in self._fields:
            fieldtype = self._instance._meta.get_field(name).__class__.__name__
            if name in self._widgets:
                widget = self.__getattribute__(self._widgets[name])
            else:
                widget = self.__getattribute__(FIELD_WIDGETS[fieldtype])
            return mark_safe(widget(name=name, value=value, fieldtype=fieldtype, itemprop=self._fields[name]))
        else:
            return value