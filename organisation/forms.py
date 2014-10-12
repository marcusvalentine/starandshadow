from django.forms import ModelForm, ChoiceField, ModelChoiceField
from django.db import models
from programming.models import Programmer, Rating, Season, Film, Gig, Event, Festival, Meeting, FilmFormat, MEETING_TYPES
from organisation.models import Minutes, BoxOfficeReturn


def custom_widgets(f):
    formfield = f.formfield()
    if isinstance(f, models.DateTimeField):
        formfield.widget.attrs.update({'class': 'dateTimePicker'})
    elif isinstance(f, models.DateField):
        formfield.widget.attrs.update({'class': 'datePicker'})
    elif isinstance(f, models.TimeField):
        formfield.widget.attrs.update({'class': 'timePicker'})
    elif isinstance(f, models.TextField):
        formfield.widget.attrs.update({'cols': '80', 'rows': '10'})
    elif isinstance(f, models.CharField):
        formfield.widget.attrs.update({'size': '82', })
    return formfield


class FormMedia(object):
    pass

#    class Media:
#        css = {
#            'all': (
#                    'jwysiwyg/jquery.wysiwyg.css',
#                    'jwysiwyg/plugins/fileManager/wysiwyg.fileManager.css',
#                    'css/forms.css',
#                    )
#        }
#        js = (
#              'jwysiwyg/jquery.wysiwyg.js',
#              'jwysiwyg/controls/wysiwyg.image.js',
#              'jwysiwyg/controls/wysiwyg.link.js',
#              'jwysiwyg/plugins/wysiwyg.fileManager.js',
#              'js/forms.js',
#              )

class SeasonForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Season
        exclude = ('programmer', 'featured', )


class SeasonAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Season
        exclude = ('approval',)


class FilmForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    certificate = ModelChoiceField(queryset=Rating.objects.all(), empty_label=None)
    filmFormat = ModelChoiceField(queryset=FilmFormat.objects.all(), empty_label=None)
    season = ModelChoiceField(queryset=Season.objects.all().order_by('title'), empty_label=None)
    formfield_callback = custom_widgets

    class Meta:
        model = Film
        exclude = ('programmer', 'featured', )


class FilmAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    certificate = ModelChoiceField(queryset=Rating.objects.all(), empty_label=None)
    filmFormat = ModelChoiceField(queryset=FilmFormat.objects.all(), empty_label=None)
    season = ModelChoiceField(queryset=Season.objects.all().order_by('title'), empty_label=None)
    formfield_callback = custom_widgets

    class Meta:
        model = Film
        exclude = ('approval',)


class GigForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Gig
        exclude = ('programmer', 'featured', )


class GigAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Gig
        exclude = ('approval',)


class EventForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Event
        exclude = ('programmer', 'featured', )


class EventAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Event
        exclude = ('approval',)


class FestivalForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Festival
        exclude = ('programmer', 'featured', )


class FestivalAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Festival
        exclude = ('approval',)


class MeetingForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets
    title = ChoiceField(choices=MEETING_TYPES)

    class Meta:
        model = Meeting
        exclude = ('programmer', )


class MeetingAdminForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets
    title = ChoiceField(choices=MEETING_TYPES)

    class Meta:
        model = Meeting
        exclude = ('approval',)


class ProgrammerForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Programmer


class MinutesForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = Minutes


class BoxOfficeReturnForm(ModelForm, FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets

    class Meta:
        model = BoxOfficeReturn