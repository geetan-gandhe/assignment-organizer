from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import BaseFormView
from django.views.generic import DetailView
from django.views.generic import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from organizer.models import Class, NotesUploadForm



def home(request):
    return render(request, 'organizer/home.html')

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
        context = {
            'course' : course
        }
        print(context)
        return render(request, 'organizer/detail.html', context)
# Create your views here.

""" 
def upload_file(request, class_name):
    course = Class.objects.get(class_name=class_name)
    context = {
        'course' : course
    }
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fs = FileSystemStorage()
        fs.save(upload.name, upload)
        return render(request, 'organizer/detail.html', context)
    return render(request, 'organizer/detail.html', context) """

def upload_file(request, class_name):
    course = Class.objects.get(class_name=class_name)
    context = {
        'course' : course,
        'notes': course.notes_set.all()
    }
    print(context)
    if request.method == 'POST':
        form = NotesUploadForm(request.POST, request.FILES)
        form.course = course
        if form.is_valid():
            form.save()
            return HttpResponse('File saved')
    else:
        form = NotesUploadForm()
    return render(request, 'organizer/detail.html', context)



from django.shortcuts import render,redirect
from .models import TodoList, Category
import datetime
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
			return redirect("/") #reloading the page
		
		if "taskDelete" in request.POST: #checking if there is a request to delete a todo
			checkedlist = request.POST["checkedbox"] #checked todos to be deleted
			for todo_id in checkedlist:
				todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
				todo.delete() #deleting todo

	return render(request, "organizer/index.html", {"todos": todos, "categories":categories})