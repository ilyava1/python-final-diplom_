from rest_framework import serializers
from .models import User, Contact, Category, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

class ContactSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(write_only=True)
    # company = serializers.PrimaryKeyRelatedField(write_only=True)
    class Meta:
        model = Contact
        fields = '__all__'
