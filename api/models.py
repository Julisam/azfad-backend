from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, max_length=255)
    username = models.EmailField(unique=False, blank=True,
                                 null=True, max_length=255)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.CharField(blank=True, null=True, max_length=200)

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


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    course_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT, null=True, blank=True)
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)  # Progress percentage (0-100)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.progress}%)"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


