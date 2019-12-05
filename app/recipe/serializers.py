from rest_framework import serializers
from core.models import Tag
from core.models import Ingredient

#Create a model serializer
#Link to tag and pull name values

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredients"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
