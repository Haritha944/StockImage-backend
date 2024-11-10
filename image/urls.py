from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BulkImageUploadView,ImageListView,LastUploadDateView,ImageDetailView,ImageViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('images/upload/', BulkImageUploadView.as_view(), name='image-upload'),
    path('images/',ImageListView.as_view(),name="image"),
    path('images/last-upload-date/', LastUploadDateView.as_view(), name='last-upload-date'),
    path('images/<int:id>/', ImageDetailView.as_view(), name='image-detail'),
]
urlpatterns += router.urls