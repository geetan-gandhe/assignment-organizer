from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms


class Class(models.Model):
    class_name = models.CharField(max_length=100, default="CS3240")
    users = models.ManyToManyField(User)
    enrollment = models.IntegerField(default=50)
    #notes = models.FileField(null=True, blank=True)
    class Meta:
            ordering = ['class_name']
    def __str__(self):
        return str(self.class_name)


class Notes(models.Model):
    file = models.FileField(upload_to='files/')
    course = models.ForeignKey(Class, related_name='notes_set', on_delete=models.CASCADE) 
    def __str__(self):
        return f"{self.file.name}"


class NotesUploadForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('file','course',)
