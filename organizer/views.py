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
from django import forms


def home(request):
    return render(request, 'organizer/home.html')

def loginPage(request):
    return render(request, 'organizer/loginPage.html')


# Create your views here.
