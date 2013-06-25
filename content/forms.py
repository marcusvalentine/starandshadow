from django.forms import ModelForm, ChoiceField, ModelChoiceField
from django.db import models
from ss.content.models import Page, Document, DOC_TYPE
from organisation.forms import FormMedia, custom_widgets

def custom_widgets(f):
    formfield = f.formfield()
    if isinstance(f, models.DateTimeField):
        formfield.widget.attrs.update({ 'class': 'dateTimePicker' })
    elif isinstance(f, models.DateField):
        formfield.widget.attrs.update({ 'class': 'datePicker' })
    elif isinstance(f, models.TimeField):
        formfield.widget.attrs.update({ 'class': 'timePicker' })
    elif isinstance(f, models.TextField):
        formfield.widget.attrs.update({ 'cols': '120', 'rows': '15' })
    elif isinstance(f, models.CharField):
        formfield.widget.attrs.update({ 'size': '118', })
    return formfield

class DocumentForm(ModelForm,FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets
    type = ChoiceField(choices=DOC_TYPE)
    class Meta:
        model = Document

class PageForm(ModelForm,FormMedia):
    error_css_class = 'errorField'
    required_css_class = 'requiredField'
    formfield_callback = custom_widgets
    class Meta:
        model = Page