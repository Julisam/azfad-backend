from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().order_by('-students')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
