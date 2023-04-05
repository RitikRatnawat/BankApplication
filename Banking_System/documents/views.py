import os.path

import boto3
from rest_framework import generics
from .serializers import FileSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.conf import settings
from dotenv import load_dotenv


# Create your views here.
class UploadView(generics.GenericAPIView):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({"message": "File Upload Unsuccessful"})

        serializer.save()

        filename = os.path.join(settings.MEDIA_ROOT, "files", request.data['filename'])
        object_name = os.path.join('files', request.data['filename'])

        s3_client = boto3.client('s3')
        s3_client.upload_file(Filename=filename,
                              Bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"),
                              Key=object_name)

        if os.path.exists(filename):
            os.remove(filename)

        return Response({"message": "File Uploaded Successfully"})
