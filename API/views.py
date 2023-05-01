from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from API.models import Data
from API.serializer import DataSerializer

import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class DataView(APIView):
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ JWTAuthentication ]

    def get(self, request, pk=None):
        try:
            user = request.user
            if pk:
                data = Data.objects.filter(owner=user, pk=pk)
                print(data == None)
            else:
                data = Data.objects.filter(owner=user)
            serializer = DataSerializer(data, many=True)
            logger.warning('GET Method is Called : '+str(datetime.datetime.now()))
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            logger.warning('GET Method HTTP_500_INTERNAL_SERVER_ERROR : '+str(datetime.datetime.now()))
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = DataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                logger.warning('POST Method is Called : '+str(datetime.datetime.now()))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.warning('POST Method HTTP_500_INTERNAL_SERVER_ERROR : '+str(datetime.datetime.now()))
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            user = request.user
            data = Data.objects.filter(owner=user, pk=pk).first()
            if not data:
                return Response({'error': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = DataSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.warning('PUT Method is Called : '+str(datetime.datetime.now()))
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.warning('PUT Method HTTP_500_INTERNAL_SERVER_ERROR : '+str(datetime.datetime.now()))
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            user = request.user
            data = Data.objects.filter(owner=user, pk=pk).first()
            if not data:
                return Response({'error': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)
            data.delete()
            logger.warning('DELETE Method is Called : '+str(datetime.datetime.now()))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.warning('DELETE Method HTTP_500_INTERNAL_SERVER_ERROR : '+str(datetime.datetime.now()))
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
