from rest_framework import serializers
from .models import Category, Genre
from django.db import IntegrityError


class CategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField()

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'This category was already created'
            })

    class Meta:
        model = Category
        fields = [
            'id', 'cat_name'
        ]


class GenreSerializer(serializers.ModelSerializer):
    gen_name = serializers.CharField()
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.cat_name

    class Meta:
        model = Genre
        fields = [
            'id', 'gen_name', 'category', 'category_name'
        ]
