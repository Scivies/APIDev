from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#import tag and serializers
from core.models import Tag
from core.models import Ingredient
from recipe import serializers

# Create your views here.
#Create List Model

class TagViewSet(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    """Manage tags in the database"""
    #Create authentication tokens to pass
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    #Query set I want to retrun
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        """Return displays in the API"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

#Add mixins that are apporpriate for your feature set.
    #Override the mixins create model to pass in a new create serializer model
    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage ingredients in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)
