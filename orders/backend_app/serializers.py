from rest_framework import serializers
from .models import Shop, Category


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'filename']


class CategorySerializer(serializers.ModelSerializer):
    shops = ShopSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'shops']
