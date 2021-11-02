from django.conf.urls import include
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from . import views

app_name = 'organizer'

urlpatterns = [
    path('classes', views.ClassListView.as_view(), name='classes'),
    path('', views.loginPage, name='index'),
    path('home/', views.home, name='homepage'),
    path('classes/<str:class_name>/', views.DetailView.custom_detail_view, name='detail'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
    path('classes/<str:class_name>/', views.upload_file, name='upload_file')]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

