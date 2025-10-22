# manga/serializers.py
from rest_framework import serializers
from .models import Series

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__' # This will include all fields from your model
        # You can also be specific:
        # fields = ['id', 'title', 'description', 'cover_image_url', 'status']