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
