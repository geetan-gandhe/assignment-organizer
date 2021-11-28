from __future__ import unicode_literals
from django.db import models
from django.db.models import fields
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from taggit.managers import TaggableManager


class Class(models.Model):
    class_name = models.CharField(max_length=100, default="CS3240")
    users = models.ManyToManyField(User, related_name="students")
    enrollment = models.IntegerField(default=50)
    class Meta:
            ordering = ['class_name']
    def __str__(self):
        return str(self.class_name)
    objects = models.Manager()


      
class Reviews(models.Model):
    class_Instructor = models.CharField(max_length=100, default="Class Instructor")
    review = models.TextField(max_length=100, default="Great class!")
    course = models.ForeignKey(Class, related_name='reviews_set', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.course)

class Notes(models.Model):
    file = models.FileField(upload_to='media/')
    course = models.ForeignKey(Class, related_name='notes_set', on_delete=models.CASCADE) 
    def __str__(self):
        return f"{self.file.name}"
    objects = models.Manager()
    tags = TaggableManager()


class NotesUploadForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('file','course',)


# Create your models here.
class Category(models.Model): # The Category table name that inherits models.Model
	name = models.CharField(max_length=100) #Like a varchar

	class Meta:
		verbose_name = ("Category")
		verbose_name_plural = ("Categories")

	def __str__(self):
		return self.name #name to be shown when called

class TodoList(models.Model): #Todolist able name that inherits models.Model
    title = models.CharField(max_length=250) # a varchar
    email = models.CharField(max_length=250,default="someone@gmail.com") # a varchar
    content = models.TextField(blank=True) # a text field 
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    category = models.ForeignKey(Category,  on_delete=models.PROTECT, default="general") # a foreignkey

class Meta:
		ordering = ["-created"] #ordering by the created field
def __str__(self):
		return self.title #name to be shown when called

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('organizer:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'