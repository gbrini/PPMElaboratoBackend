from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ( 'id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name' )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError( { "password": "Passwords fields didn't match." } )
        
        return attrs

    def create(self, validated_data):
        del validated_data['password2']

        user = CustomUser.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ( 'id', 'username', 'role', 'email', 'first_name', 'last_name' )

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ( 'role', )

class ThrottleInfoSerializer(serializers.Serializer):
    rate = serializers.CharField()
    limit = serializers.IntegerField()
    remaining = serializers.IntegerField()
    reset_in = serializers.IntegerField()

class UserThrottleProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.CharField()
    throttle = ThrottleInfoSerializer()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError( { "confirm_new_password": "New passwords do not match" } )

        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError( { "new_password": "New passwordsd cannot be the same as the old one" } )

        return data