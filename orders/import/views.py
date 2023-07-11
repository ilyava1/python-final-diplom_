import os
from django.http import JsonResponse
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader
from backend_app.models import Shop, Category, Product, ProductInfo
from backend_app.models import Parameter, ProductParameter


class PriceImport(APIView):
    """
    Класс для загрузки/обновления данных о прайсе магазина.
    """
    def post(self, request, *args, **kwargs):
        file_path = os.getcwd() + '\\shop1.yaml'
        fl = open(file_path, 'r', encoding='utf-8')
        dict_from_yaml = load_yaml(fl, Loader=Loader)
        fl.close()

        # Загружаем магазин с его атрибутами:
        shop_object = dict_from_yaml['shop'][0]
        shop = Shop(id=shop_object['id'], name=shop_object['name'],
                    url=shop_object['url'], filename=shop_object['filename'])
        shop.save()

        # Загружаем категории:
        category_objects = dict_from_yaml['categories']

        for category_object in category_objects:
            type_x = int(category_object['id'])
            category = Category(id=category_object['id'], name=category_object['name'])
            category.shops.add(shop.id)
            category.save()

        # Загружаем товары:
        goods_objects = dict_from_yaml['goods']
        for good_object in goods_objects:
            product = Product(id=good_object['id'], name=good_object['name'],
                                      category_id=good_object['category'])
            product.save()

            # Загружаем информацию о товарах
            existing_prod_info = list(ProductInfo.objects.filter(product_id=product.id))
            if existing_prod_info == []:
                # Если информации по продукту нет - добавляем ее в базу
                product_info = ProductInfo(product_id=good_object['id'],
                                           shop_id=shop.id,
                                           name=good_object['model'],
                                           quantity=good_object['quantity'],
                                           price=good_object['price'],
                                           price_rrc=good_object['price_rrc'])
            else:
                # Если информация по продукту есть - обновляем её
                product_info = ProductInfo(id=existing_prod_info[0].id,
                                           product_id=good_object['id'],
                                           shop_id=shop.id,
                                           name=good_object['model'],
                                           quantity=good_object['quantity'],
                                           price=good_object['price'],
                                           price_rrc=good_object['price_rrc'])
            product_info.save()

            # Загружаем информацию о параметрах и параметрах продукта
            for parameter_name, parameter_value in good_object['parameters'].items():
                existing_parameter = list(Parameter.objects.filter(name=parameter_name))
                if existing_parameter == []:
                    parameter = Parameter(name=parameter_name)
                    parameter.save()
                    product_parameter = ProductParameter(product_info_id=product_info.id,
                                                         parameter_id=parameter.id,
                                                         value=parameter_value)
                else:
                    product_parameter = ProductParameter(product_info_id=product_info.id,
                                                         parameter_id=existing_parameter[0].id,
                                                         value=parameter_value)
                product_parameter.save()


        return JsonResponse({'Status': True,
                             'File': f'Загрузка прайса магазина {shop.name} произведена'})


    def get(self, request, *args, **kwargs):
        return JsonResponse({'Status': False,
                             'Errors': 'Dump price procedure stopper'})