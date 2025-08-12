from django.contrib import admin
from .models import Course, Cart, Enrollment, BlogPost

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'created_at']
    list_filter = ['created_at', 'price']
    search_fields = ['title', 'description']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__email', 'course__title']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress', 'enrolled_at']
    list_filter = ['enrolled_at', 'progress']
    search_fields = ['user__email', 'course__title']
    list_editable = ['progress']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['published']
