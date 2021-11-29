from __future__ import print_function, unicode_literals
from calendar import calendar
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
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

from django.core.mail import send_mail



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

#Sources for tags: https://django-taggit.readthedocs.io/en/latest/, https://hackernoon.com/how-to-add-tags-to-your-models-in-django-django-packages-series-1-4y1b32sf, https://aymane-talibi-at.medium.com/how-to-add-tags-in-django-19090e8d05d3


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

#Sources for file upload: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/, https://www.askpython.com/django/upload-files-to-django, https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms

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

# Create your views here.

def index(request): #the index view

    todos = TodoList.objects.all() #quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager

    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date

            email= request.user.email

            category = request.POST["category_select"] #category
            content = title + " -- " + date + " " + category #content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save() #saving the todo 

            sender_email = "assignmentorganizera27@gmail.com"
            receiver_email = "williamsgchenelle@gmail.com"
            password = "GroupA27Pass!"

            
            message2 = MIMEMultipart("alternative")
            message2["Subject"] = "You have a new task!"
            message2["From"] = sender_email
            message2["To"] = email
            

            # Create the plain-text and HTML version of your message
            html = """\
            <html>
            <body>
                <p>Hi,<br>
                How are you?<br>
                <a href="http://www.realpython.com">Real Python</a> 
                has many great tutorials.
                </p>
            </body>
            </html>
            """
            
            body = {
            'Greeting': "Hello!",
            'Sen': "A new task has been added. Your task details are below: ",
            's': " ",
            'n1': "Description",
			'Task title': title, 
            's1': " ",
            'n2': "Category",
			'Category': category, 
            's2': " ",
            'n3': "Due Date",
			'Due Date': date, 
            's3': " ",
            'endgreeting': "Thank you",
            'endgreeting2': "Assignment and Task Organizer (A27)",
			}
            
            body2="\n".join(body.values())
            d=MIMEText(body2, "plain")
            message2.attach(d)
            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                sender_email, receiver_email, message2.as_string()
            )
            return redirect("/index") #reloading the page

        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            print(checkedlist)
            todo_id_f = ""
            for todo_id in checkedlist:
                todo_id_f = todo_id_f + str(todo_id)
            print(todo_id_f, "todo")
            todo = TodoList.objects.filter(id=int(todo_id_f))
            todo.delete() #deleting todo
    return render(request, "organizer/index.html", {"todos": todos, "categories":categories})


    
class CalendarView(generic.ListView):
    model = Event
    template_name = 'organizer/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        print(context)
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

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('organizer:calendar'))
    return render(request, 'organizer/event.html', {'form': form})


