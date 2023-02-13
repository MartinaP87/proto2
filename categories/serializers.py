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

        # def get_is_owner(self, obj):
        # request = self.context['request']
        # return request.user == obj.profile.owner

    class Meta:
        model = Genre
        fields = [
            'id', 'gen_name', 'gen_name_text', 'category'
        ]
