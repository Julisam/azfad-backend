from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'created_at']
    list_filter = ['created_at', 'price']
    search_fields = ['title', 'description']
