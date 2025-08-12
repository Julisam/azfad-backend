from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Course, CustomUser, Cart, Enrollment, BlogPost
from .serializers import CourseSerializer, ProfileSerializer, CartSerializer, EnrollmentSerializer, BlogPostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().order_by('-students')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = ProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# Cart Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    course_id = request.data.get('course_id')
    if not course_id:
        return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        return Response({'error': 'Already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already in cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, course=course)
    if not created:
        return Response({'error': 'Course already in cart'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CartSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = Cart.objects.filter(user=request.user, paid=False).order_by('-added_at')
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart_item_ids = request.data.get('cart_items', [])
    if not cart_item_ids:
        return Response({'error': 'No cart items provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_items = Cart.objects.filter(id__in=cart_item_ids, user=request.user)
    
    # Create enrollments and remove from cart
    enrollments_created = []
    for cart_item in cart_items:
        # Check if not already enrolled
        if not Enrollment.objects.filter(user=request.user, course=cart_item.course).exists():
            enrollment = Enrollment.objects.create(
                user=request.user,
                course=cart_item.course,
                cart = cart_item
            )
            enrollments_created.append(enrollment)
        cart_item.paid = True
        cart_item.save()

    
    return Response({
        'message': f'Successfully enrolled in {len(enrollments_created)} courses',
        'enrollments': len(enrollments_created)
    }, status=status.HTTP_200_OK)


# My Courses Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-enrolled_at')
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


# Blog Views
class BlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(published=True).order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
