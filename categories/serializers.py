from rest_framework import serializers
from .models import Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField()

    class Meta:
        model = Category
        fields = [
            'id', 'cat_name'
        ]


class GenreSerializer(serializers.ModelSerializer):
    gen_name = serializers.CharField()
    category = serializers.ReadOnlyField(source='category.cat_name')

    class Meta:
        model = Genre
        fields = [
            'id', 'gen_name', 'category'
        ]
