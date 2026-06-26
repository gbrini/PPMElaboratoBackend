from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

ROLE_CHOICES = (
    ( 'standard', 'Standard' ),
    ( 'premium', 'Premium' ),
    ( 'admin', 'Admin' )
)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='standard')

    class Meta:
        model = CustomUser
        fields = ( 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role' )

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