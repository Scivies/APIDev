from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

"""Serializer will inherate from the imported serialiers module. This module
will do the database conversions of the user for us.
"""

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
#Specify what model you want to base your serializer on.
        model = get_user_model()
#Specify the fields you want to include in the serializer.
#These are the json fields we want passed and make accessible
#Add additional fields/Params for the API to the fields varialbe e.g. 'Date of Birth'
        fields = ('email', 'password', 'name')
#Imliment the test for password length to test the password is valid via length
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

#Create and Pass the validated data
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

#Create function to update password_validation
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """"Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate the attributes of the user email/password"""
        email = attrs.get('email')
        password = attrs.get('password')

        """Authenticate the request"""
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serialiers.validationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
