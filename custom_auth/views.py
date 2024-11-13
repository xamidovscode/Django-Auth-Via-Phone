from rest_framework import generics
from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
