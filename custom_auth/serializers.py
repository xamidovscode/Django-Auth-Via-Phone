from rest_framework import serializers
from . import models
import random
from django.core.cache import cache

def generate_random_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(5)])


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
        if user:
            user.password = validated_data['password1']
            user.save()
            instance = user
        else:
            instance = models.CustomUser.objects.create_user(phone=validated_data['phone'], password=validated_data['password1'])
        code = generate_random_number()
        print(code)
        cache.set(instance.phone, code, timeout=120)
        return instance


class CodeVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        request = self.context.get('request')
        cache_code = cache.get(request.user.phone)
        if not cache_code:
            raise serializers.ValidationError({"code": "Code expired"})
        elif cache_code != attrs['code']:
            raise serializers.ValidationError({"code": "Code is not correct"})
        return attrs
