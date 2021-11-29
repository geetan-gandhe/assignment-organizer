from django import forms
from organizer.models import Notes
from django.forms import ModelForm, DateInput
from organizer.models import Event

#Sources: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/, https://www.askpython.com/django/upload-files-to-django, https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms
class NotesUploadForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = Notes
        fields = ('file', 'tags')

class CreateNotes(forms.Form):
    file = forms.FileField()

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)