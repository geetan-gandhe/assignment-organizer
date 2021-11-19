from __future__ import unicode_literals
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
from organizer.forms import NotesUploadForm
from .models import TodoList, Category

from datetime import datetime
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar
import datetime


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

def upload_file(request, class_name):
    this_course = Class.objects.get(class_name=class_name)
    template = loader.get_template('organizer/detail.html')
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
        'notes': this_course.notes_set.all()
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




# Create your views here.

def index(request): #the index view
	todos = TodoList.objects.all() #quering all todos with the object manager
	categories = Category.objects.all() #getting all categories with object manager
	if request.method == "POST": #checking if the request method is a POST
		if "taskAdd" in request.POST: #checking if there is a request to add a todo
			title = request.POST["description"] #title
			date = str(request.POST["date"]) #date
			category = request.POST["category_select"] #category
			content = title + " -- " + date + " " + category #content
			Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
			Todo.save() #saving the todo 
			return redirect("/index") #reloading the page
		
		if "taskDelete" in request.POST: #checking if there is a request to delete a todo
			checkedlist = request.POST["checkedbox"] #checked todos to be deleted
			for todo_id in checkedlist:
				todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
				todo.delete() #deleting todo

	return render(request, "organizer/index.html", {"todos": todos, "categories":categories})

def index2(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'organizer/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()