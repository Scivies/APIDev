from rest_framework import serializers
from core.models import Tag
from core.models import Ingredient
from core.models import Recipe

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

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipes"""
    #add class variables as primary key relations
    #This will only use the ingredients ID : will add details
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'tags', 'price', 'ingredients',
                    'link', 'time_minutes'
        )
        read_only_fields = ('id',)
