from django.urls import path
from .views import BulkImageUploadView,ImageListView,LastUploadDateView,ImageDetailView

urlpatterns = [
    path('images/upload/', BulkImageUploadView.as_view(), name='image-upload'),
    path('images/',ImageListView.as_view(),name="image"),
    path('images/last-upload-date/', LastUploadDateView.as_view(), name='last-upload-date'),
    path('images/<int:id>/', ImageDetailView.as_view(), name='image-detail'),
]