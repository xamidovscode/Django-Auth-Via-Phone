from rest_framework import generics
from . import serializers
from . import models


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
