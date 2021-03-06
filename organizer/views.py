from __future__ import print_function, unicode_literals
from calendar import calendar
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import BaseFormView, CreateView
from django.views.generic import DetailView
from django.views.generic import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from taggit.models import Tag
from django.template import loader

from organizer.models import Class, Notes, Reviews
from organizer.forms import EventForm, NotesUploadForm
from .models import TodoList, Category

import requests
from datetime import date, datetime, timedelta
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar
from .forms import EventForm
import datetime
import calendar
import sendgrid
import os

from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    if request.user.is_authenticated:
        context = {
        "schedule": request.user.students.all()
        }
        return render(request, 'organizer/home.html', context)
    else:
        context = {
        }
    return render(request, 'organizer/home.html', context)

def loginPage(request):
    return render(request, 'organizer/loginPage.html')

class ClassListView(generic.ListView):
    template_name = 'organizer/classes.html'
    context_object_name = 'classes_list'

    def get_queryset(self):
        return Class.objects.all().values('class_name')

## REFERENCES
# Title: Django-taggit
# Author: Alex Gaynor and individual contributors
# Date: n/a
# Code version: Revision 12b899ed.
# URL: https://django-taggit.readthedocs.io/en/latest/
# Software License: BSD-3

# Title: How to add tags in Django
# Author:Aymane Talibi
# Date: September 16th, 2020
# Code version: n/a
# URL: https://aymane-talibi-at.medium.com/how-to-add-tags-in-django-19090e8d05d3
# Software License: n/a

# Title: How to add tags to your models in Django
# Author: Hackernoon
# Date: December 14th 2019
# Code version: n/a
# URL: https://hackernoon.com/how-to-add-tags-to-your-models-in-django-django-packages-series-1-4y1b32sf
# Software License: BSD-3

class DetailView(View):
    def custom_detail_view(request, class_name):
        #try:
        course = Class.objects.get(class_name=class_name)
        common_tags = Notes.tags.most_common()[:4]
        context = {
            'course': course,
            'notes': course.notes_set.all(),
            'reviews': course.reviews_set.all(),
            'common_tags': common_tags,
        }

        print(context)
        return render(request, 'organizer/detail.html', context)
    def tagged_detail_view(request, class_name, slug):
        #try:
        course = Class.objects.get(class_name=class_name)
        tag = get_object_or_404(Tag, slug=slug)
        common_tags = Notes.tags.most_common()[:4]
        context = {
            'course': course,
            'notes': course.notes_set.filter(tags=tag),
            'reviews': course.reviews_set.all(),
            'slug': slug,
            'common_tags': common_tags,
        }

        print(context)
        return render(request, 'organizer/detail.html', context)

def profile_view(request):
    context = {
        "schedule": request.user.students.all()
    }
    return render(request, 'organizer/profile.html', context)


def leave_class(request, class_name):
    this_course = Class.objects.get(class_name=class_name)
    if request.method == 'POST':
        student = request.user
        this_course.users.remove(student)
        this_course.save()

    context = {
        "schedule": request.user.students.all()
    }
    return render(request, 'organizer/profile.html', context)

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

def upload_file(request, class_name):
    this_course = Class.objects.get(class_name=class_name)
    template = loader.get_template('organizer/detail.html')
    common_tags = Notes.tags.most_common()[:4]

    if request.method == 'POST':
        form = NotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            #instance = Notes(file = request.FILES['file'],course=this_course)
            #instance.save()
            #print("file saved")
            context = {
                'form': form,
                'course': this_course,
                'notes': this_course.notes_set.all()
            }
            instance=form.save(commit=False)
            instance.course=this_course
            instance.save()
            for tag in form.cleaned_data['tags']:
                instance.tags.add(tag)
            return HttpResponseRedirect(reverse('organizer:detail', args=(class_name,)))
    else:
        form = NotesUploadForm()
    context = {
        'form': form,
        'course': this_course,
        'notes': this_course.notes_set.all(),
        'common_tags': common_tags,
    }
    return render(request, 'organizer/detail.html', context)



class ReviewListView(CreateView):
    model = Reviews
    template_name = 'organizer/reviews.html'
    context_object_name = 'review_list'
    success_url = "/organizer/classes"
    fields = ['class_Instructor', 'course', 'review']

    def get_queryset(self):
        return Reviews.objects.all().values()


def join_class(request, class_name):
    this_course = Class.objects.get(class_name=class_name)
    if request.method == 'POST':
        student = request.user
        this_course.users.add(student)
        this_course.save()

    context = {
        'course': this_course,
        'notes': this_course.notes_set.all()
    }
    return render(request, 'organizer/detail.html', context)


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from django.conf import settings

## REFERENCES
# Title: How to Build a TodoApp with Django
# Author: Oyetoke Tobi Emmanuel
# Date: April 23rd, 2018
# Code version: n/a
# URL: https://medium.com/fbdevclagos/how-to-build-a-todo-app-with-django-17afdc4a8f8c
# Software License: n/a

# Title: User Registration in Django using Google OAuth
# Author: Geoffrey Mungai
# Date: December 18th, 2020
# Code version: n/a
# URL: https://www.section.io/engineering-education/django-google-oauth/
# Software License: n/a

@login_required
def index(request): 
    todos = TodoList.objects.filter(user=request.user)

    categories = Category.objects.all() 
    print(request.user.email)
    if request.user.is_authenticated:
        email= request.user.email

    if request.method == "POST": 
        if "taskAdd" in request.POST: 
            title = request.POST["description"] 
            date = str(request.POST["date"]) 
            category = request.POST["category_select"] 
            content = title + " -- " + date + " " + category 
            user=request.user
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category), user=user)
            Todo.save() 


            sg = sendgrid.SendGridAPIClient(api_key=('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'))
            data = {
            "personalizations": [
                {
                "to": [
                    {
                    "email": email
                    }
                ],
                "subject": "You have a new task!",
                "substitutions": {
                    "-title-": title,
                    "-cat-": category,
                    "-date-":date,
                                },
                }
            ],
            "from": {
                "email": "assignmentorganizera27@gmail.com"
            },
            "content": [
                {
                "type": "text/html",
                'value':  "<html>\n  <head></head>\n  <body>\n    <p>Hello! You have a new task.\n </p> <p>Good job staying organized! The details of your new task are below:\n</p>    <p> Title: -title-\n</p> <p>Category: -cat- \n</p> <p> Date: -date-\n</p>\n <p>Your Assignment Organizer,</p> <p> Group A27 </p> </body>\n</html>"
                          },
                
                        ]
            }
            
            
            response = sg.client.mail.send.post(request_body=data)
            print(response.status_code)
            print(response.body)
            print(response.headers)
                       
            return redirect("/index") 

        if "taskDelete" in request.POST:
            checkedlist = request.POST["checkedbox"] 
            print(checkedlist)
            todo_id_f = ""
            for todo_id in checkedlist:
                todo_id_f = todo_id_f + str(todo_id)
            print(todo_id_f, "todo")
            todo = TodoList.objects.filter(id=int(todo_id_f))
            todo.delete() 
    return render(request, "organizer/index.html", {"todos": todos, "categories":categories})

## REFERENCES
# Title: How to create a calendar using django
# Author: Hui Wen
# Date: 24 July 2018
# Code version: n/a
# URL: https://hackernoon.com/how-to-add-tags-to-your-models-in-django-django-packages-series-1-4y1b32sf
# Software License: BSD-3

class CalendarView(generic.ListView):
    model = Event()
    template_name = 'organizer/calendar.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset=  Event.objects.all().filter(user=self.request.user)
            return queryset
        else:   
            return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        if self.request.user.is_authenticated:
            html_cal = cal.formatmonth(user=self.request.user, withyear=True)
            context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if request.POST:  
        print("here1")
        if "submit" in request.POST and form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            return HttpResponseRedirect(reverse('organizer:calendar'))
        elif "delete" in request.POST:
            print("here")
            if event_id:
                to_delete = Event.objects.filter(id=event_id)
                to_delete.delete()
            return HttpResponseRedirect(reverse('organizer:calendar'))
        else:
            return HttpResponseRedirect(reverse('organizer:calendar'))
    return render(request, 'organizer/event.html', {'form': form})



