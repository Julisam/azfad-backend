from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, max_length=255)
    username = models.EmailField(unique=False, blank=True,
                                 null=True, max_length=255)

    USERNAME_FIELD = 'email'


    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Create your models here.
class Course(models.Model):

    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=100, 
                             choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
                             )
    description = models.TextField()
    duration = models.CharField(max_length=100)
    students = models.PositiveIntegerField(default=4)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.7)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    images = models.CharField(blank=True, null=True, max_length=200)
    
    def __str__(self):
        return self.title + " " + self.level



