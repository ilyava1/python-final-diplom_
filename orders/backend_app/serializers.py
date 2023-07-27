from rest_framework import serializers
from .models import Category, Company, Product, Parameter, ProductParameter, ProductInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('id',)


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductInfoSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=True)
    product = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'product', 'company', 'name', 'quantity', 'price', 'price_rrc')
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer(read_only=True, many=True)
    product_info = ProductInfoSerializer(read_only=True, many=True)
    class Meta:
        model = ProductParameter
        fields = ('product_info', 'parameter', 'value',)


