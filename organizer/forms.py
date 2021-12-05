from django import forms
from organizer.models import Notes
from django.forms import ModelForm, DateInput
from organizer.models import Event

## REFERENCES
# Title: File uploads
# Author: django documentations
# Date: n/a
# Code version: n/a
# URL: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
# Software License: BSD-3

# Title: File Uploads to Django
# Author: AskPython
# Date: n/a
# Code version: n/a
# URL: https://www.askpython.com/django/upload-files-to-django
# Software License: n/a

# Title: Uploading A file in django with ModelForms
# Author: n/a
# Date: 2013
# Code version: n/a
# URL: https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms
# Software License: n/a

class NotesUploadForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = Notes
        fields = ('file', 'tags')

class CreateNotes(forms.Form):
    file = forms.FileField()

## REFERENCES
# Title: How to create a calendar using django
# Author: Hui Wen
# Date: 24 July 2018
# Code version: n/a
# URL: https://hackernoon.com/how-to-add-tags-to-your-models-in-django-django-packages-series-1-4y1b32sf
# Software License: BSD-3

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'
    exclude = ('user',)


  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
   

  
