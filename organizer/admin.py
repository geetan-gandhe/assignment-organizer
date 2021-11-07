from django.contrib import admin
from . import models

from organizer.models import Class, Notes, NotesUploadForm, TodoList, Category

# Register your models here.
admin.site.register(Class)
admin.site.register(Notes)

class TodoListAdmin(admin.ModelAdmin):
    	list_display = ("title", "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)

admin.site.register(models.TodoList, TodoListAdmin)
admin.site.register(models.Category, CategoryAdmin)

