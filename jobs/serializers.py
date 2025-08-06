from rest_framework import serializers
from .models import Job, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'description',
            'salary', 'date_posted', 'is_active', 'category', 'category_id'
        ]