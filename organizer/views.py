from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import BaseFormView, CreateView
from django.views.generic import DetailView
from django.views.generic import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from organizer.models import Class, Notes, Reviews
from organizer.forms import NotesUploadForm



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
            'course': course,
            'notes': course.notes_set.all(),
            'reviews': course.reviews_set.all(),
        }

        print(context)
        return render(request, 'organizer/detail.html', context)


def upload_file(request, class_name):
    this_course = Class.objects.get(class_name=class_name)
    print(request.method)
    if request.method == 'POST':
        form = NotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Notes(file = request.FILES['file'],course=this_course)
            instance.save()
            print("file saved")
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

