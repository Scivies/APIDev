from rest_framework import serializers
from django.contrib.auth import get_user_model

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
