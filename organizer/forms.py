from django import forms
from organizer.models import Class, Notes

class NotesUploadForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = Notes
        fields = ('file',)

class CreateNotes(forms.Form):
    file = forms.FileField()