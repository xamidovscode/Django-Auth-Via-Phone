from rest_framework import serializers
from . import models
import random
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


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
        """
        just send code to the phone number
        """
        cache.set(instance.phone, code, timeout=120)
        print(code)
        return instance


class CodeVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        user = self.context.get('user')
        cache_code = cache.get(user.phone)
        if not cache_code:
            raise serializers.ValidationError({"code": "Code expired"})
        elif cache_code != attrs['code']:
            raise serializers.ValidationError({"code": "Code is not correct"})
        return attrs


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True, write_only=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)

    def validate(self, attrs):
        user = models.CustomUser.objects.filter(phone=attrs['phone'], status="code_verified").first()
        if not user:
            raise serializers.ValidationError({"phone": "You have not registered in the system before, please register"})
        elif not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": "The password was entered incorrectly"})
        return attrs


class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255, required=True, write_only=True)

    def create(self, validated_data):
        token = validated_data.pop("refresh_token")
        try:
            refresh_token = RefreshToken(token)
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.create(token=outstanding_token)
        except Exception as e:
            raise serializers.ValidationError({"msg": e})
        return validated_data

