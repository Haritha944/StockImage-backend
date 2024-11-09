from rest_framework import serializers
from .models import Image

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'title', 'order']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'image': {'required': False}}  # 
    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
