from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Shop, Category
from .serializers import ShopSerializer, CategorySerializer
from rest_framework.renderers import JSONRenderer


class ShopView(APIView):
    def get(self, request, pk=0, *args, **kwargs):
        """
        Функция обработки get-запросов на получение объектов типа Shop.
        Если параметр pk не перадан, то по умолчанию его значение
        присваивается =0 и функция извлекает список всех магазинов.
        Иначе функция возвращает данные магазина, id которого =pk
        """
        # Shop.objects.create(name='Мобилизация', url='http://mobilization.ru', filename='qwerty.txt')
        if pk == 0:
            shops = Shop.objects.all()
            serializer = ShopSerializer(shops, many=True)
            return Response(serializer.data)
        else:
            shop = Shop.objects.filter(id=pk)
            ser = ShopSerializer(shop, many=True)
            return Response(ser.data)


class CategoryView(APIView):
    def get(self, request, pk=0, *args, **kwargs):
        """
        Функция обработки get-запросов на получение объектов типа Category.
        Если параметр pk не перадан, то по умолчанию его значение
        присваивается =0 и функция извлекает список всех категорий.
        Иначе функция возвращает данные категории, id которой =pk
        """
        Category.objects.create(name='Аксессуары', )
        if pk == 0:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        else:
            category = Category.objects.filter(id=pk)
            ser = CategorySerializer(category, many=True)
            return Response(ser.data)