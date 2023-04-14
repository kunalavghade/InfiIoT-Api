from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from API.models import Data
from API.serializer import DataSerializer


class DataView(APIView):
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ JWTAuthentication ]

    def get(self, request):
        user = request.user
        data = Data.objects.filter(owner=user)
        serializer = DataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        user = request.user
        data = Data.objects.filter(owner=user, pk=pk).first()
        if not data:
            return Response({'error': 'Data not found.'}, status=404)
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = request.user
        data = Data.objects.filter(owner=user, pk=pk).first()
        if not data:
            return Response({'error': 'Data not found.'}, status=404)
        data.delete()
        return Response(status=204)
