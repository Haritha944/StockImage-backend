from django.db import models
from account.models import CustomUser
# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='image_uploads')  # Add a user relationship
    image = models.ImageField(upload_to='uploads/')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)  # This will be used for drag and drop reordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order','-created_at'] 