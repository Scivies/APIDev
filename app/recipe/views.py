from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#import tag and serializers
from core.models import Tag
from recipe import serializers

# Create your views here.
#Create List Model

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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
        
