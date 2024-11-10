from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Image
from django.db import transaction
from .serializers import ImageUploadSerializer
import logging
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Max

# Create your views here.
class BulkImageUploadView(APIView):
    permission_classes = [IsAuthenticated] 
    parser_classes = [MultiPartParser, FormParser] 
    def post(self, request):
        logging.info(f"Request data: {request.data}")
        logging.info(f"Request files: {request.FILES}")
        titles_data = request.data.getlist('titles')
        images_data = request.FILES.getlist('images')  # Get the list of images from the request
        if len(images_data) != len(titles_data):
            return Response({"message": "The number of images and titles must match."}, status=status.HTTP_400_BAD_REQUEST)
        if not images_data:
            return Response({"message": "No images provided."}, status=status.HTTP_400_BAD_REQUEST)
        image_objects = []
        for i in range(len(images_data)):
            image = images_data[i]
            title = titles_data[i]
            # Now create an image object (assuming an Image model with a title and image fields)
            image_objects.append({
                'image': image,
                'title': title,
                'user': request.user.id
            })

        try:
            with transaction.atomic():
                serializer = ImageUploadSerializer(data=image_objects, many=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Images uploaded successfully."}, status=status.HTTP_201_CREATED)
                else:
                    logging.error(f"Validation errors: {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"An error occurred during bulk image upload: {str(e)}")
            return Response({"message": "An error occurred while uploading images."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ImageListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        image=Image.objects.filter(user=request.user).order_by('-created_at')
        serializer=ImageUploadSerializer(image,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class LastUploadDateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        last_upload = Image.objects.filter(user=request.user).aggregate(Max('created_at'))['created_at__max']
        return Response({"last_upload_date": last_upload}, status=status.HTTP_200_OK)

class ImageDetailView(APIView):
    def put(self,request,id,format=None):
        try: 
            image = Image.objects.get(id=id)
        except Image.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        userr = image.user
        print(userr)
        print("Request data:", request.data)
        print("Request FILES:", request.FILES)
        mutable_data = request.data.copy()
        mutable_data['user'] = userr.id
        if 'image' in request.FILES:
            mutable_data['image'] = request.FILES['image']
            if image.image:
                image.image.delete(save=False)
        elif 'image' in mutable_data:
            del mutable_data['image']
        serializer = ImageUploadSerializer(image,data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        try:
            image=Image.objects.get(id=id)
        except Image.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)