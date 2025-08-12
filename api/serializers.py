from rest_framework import serializers
from .models import Course, CustomUser, Cart, Enrollment, BlogPost

class CourseSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_price(self, obj):
        return f"₦{obj.price:,.0f}"

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'middlename', 'email', 'phone', 'address', 'bio', 'image']
        read_only_fields = ['email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['email'].split('@')[0].lower(),
            email=validated_data['email'].lower(),
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize(),
            password=validated_data['password'],
        )
        return user


class CartSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'course', 'added_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrolled_at', 'progress']


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.first_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author_name', 'image', 'created_at']