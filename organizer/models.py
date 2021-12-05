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
    days = models.CharField(max_length=100, default="Monday/Wednesday/Friday")
    timing = models.CharField(max_length=100, default="11:00-12:15")
    class Meta:
            ordering = ['class_name']
    def __str__(self):
        return str(self.class_name)
    objects = models.Manager()


      
class Reviews(models.Model):
    class_Instructor = models.CharField(max_length=100, default="Class Instructor", blank=False)
    review = models.TextField(max_length=100, default="Great class!", blank=False)
    course = models.ForeignKey(Class, related_name='reviews_set', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return str(self.course)

#Sources for file upload: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/, https://www.askpython.com/django/upload-files-to-django, https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms
#Sources for tags: https://django-taggit.readthedocs.io/en/latest/, https://hackernoon.com/how-to-add-tags-to-your-models-in-django-django-packages-series-1-4y1b32sf, https://aymane-talibi-at.medium.com/how-to-add-tags-in-django-19090e8d05d3

class Notes(models.Model):
    file = models.FileField(upload_to='media/')
    course = models.ForeignKey(Class, related_name='notes_set', on_delete=models.CASCADE) 
    def __str__(self):
        return f"{self.file.name}"
    objects = models.Manager()
    tags = TaggableManager()




##https://medium.com/fbdevclagos/how-to-build-a-todo-app-with-django-17afdc4a8f8c
class Category(models.Model): 
	name = models.CharField(max_length=100) 
	class Meta:
		verbose_name = ("Category")
		verbose_name_plural = ("Categories")

	def __str__(self):
		return self.name 

class TodoList(models.Model): 
    title = models.CharField(max_length=300) 
    email = models.CharField(max_length=250,default="someone@gmail.com")
    category = models.ForeignKey(Category,  on_delete=models.PROTECT, default="general") 
    classSection=models.CharField(max_length=200,default="No Class")
    content = models.TextField(blank=True) 
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) 


class Meta:
		ordering = ["-created"] 
def __str__(self):
		return self.title 

### Source: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        url = reverse('organizer:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
