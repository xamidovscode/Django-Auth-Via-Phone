from rest_framework import serializers
from . import models


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True, write_only=True)
    password1 = serializers.CharField(max_length=255, required=True, write_only=True)
    password2 = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):
        if models.CustomUser.objects.filter(phone=attrs['phone'], status="code_verified").exists():
            raise serializers.ValidationError({"phone": "This phone number already in use"})
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Passwords are not equal"})
        return attrs

    def create(self, validated_data):
        user = models.CustomUser.objects.filter(phone=validated_data['phone']).first()
        if models.CustomUser.objects.filter(phone=validated_data['phone']).first():
            user.password = validated_data['password']
            user.save()
            instance = user
        else:
            instance = models.CustomUser.objects.create_user(phone=validated_data['phone'], password=validated_data['password1'])
        return instance


