from rest_framework import generics
from . import serializers
from rest_framework import status
from rest_framework.response import Response


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        tokens = user.tokens() if callable(user.tokens) else user.tokens

        data = {
            "phone": str(user.phone),
            "tokens": tokens
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CodeVerificationAPIView(generics.CreateAPIView):
    serializer_class = serializers.CodeVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        user.status = "code_verified"
        user.save()
        tokens = user.tokens() if callable(user.tokens) else user.tokens

        data = {
            "phone": str(self.request.user.phone),
            "tokens": tokens
        }
        return Response(data=data, status=status.HTTP_200_OK)
