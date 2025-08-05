from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_price(self, obj):
        return f"₦{obj.price:,.0f}"