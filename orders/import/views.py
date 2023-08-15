import os
from django.http import JsonResponse
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader
from backend_app.models import Company, Category, Product, ProductInfo
from backend_app.models import Parameter, ProductParameter, Contact


class PriceImport(APIView):
    """
    Класс для загрузки/обновления данных о прайсе магазин.
    """
    def post(self, request, *args, **kwargs):
        # Если пользователь не аутентифицирован - отказ в продолжении операции
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        # Формируем список компаний типа "поставщик", по которым пользователь
        # зарегистрирован в качестве контакта.
        # Если список пуст - отказ в продолжении операции
        company_list = []
        suppliers = Company.objects.filter(type='supplier')
        for company in suppliers:
            user_contact = Contact.objects.filter(user=request.user,
                                                  company=company)
            if user_contact.exists():
                company_list.append(company.company_name)

        # Если пользователь авторизован, читаем файл с прайсом
        file_path = os.getcwd() + '\\supplier1.yaml'
        fl = open(file_path, 'r', encoding='utf-8')
        dict_from_yaml = load_yaml(fl, Loader=Loader)
        fl.close()

        # Проверяем наличие поставщика в базе.
        # Если в базе нет такого поставщика - отказ в продолжении операции
        supplier_object = dict_from_yaml['supplier'][0]
        try:
            supplier = Company.objects.get(id=supplier_object['id'])
        except:
            str = f'Company with id={supplier_object["id"]} ' \
                  f'{supplier_object["name"]} has not been registered ' \
                  f'in the database yet. Сomplete the registration before' \
                  f' loading price'
            return JsonResponse({'Loading status': False,
                                 'Message':  str}, status=404)

        # Если поставщик зарегистрирован, проверяем по тому ли поставщику
        # зарегистрирован пользователь.
        # Если не по тому - отказ в продолжении операции
        if supplier_object['name'] not in company_list:
            str = f'Price from company {supplier_object["name"]}, ' \
                  f'but you registered from following company(ies) ' \
                  f'{company_list}'
            return JsonResponse({'Loading status': False,
                                 'Message': str}, status=403)

        # Далее приступаем к загрузке прайса
        # Снчала загружаем категории:
        category_objects = dict_from_yaml['categories']

        for category_object in category_objects:
            category = Category(id=category_object['id'],
                                name=category_object['name'])
            category.save()
            category.companies.add(supplier_object['id'])

        # Загружаем товары:
        goods_objects = dict_from_yaml['goods']
        for good_object in goods_objects:
            product = Product(id=good_object['id'], name=good_object['name'],
                                      category_id=good_object['category'])
            product.save()

            # Загружаем информацию о товарах
            existing_prod_info = list(ProductInfo.objects.filter(
                product_id=product.id))
            if existing_prod_info == []:
                # Если информации по продукту нет - добавляем ее в базу
                product_info = ProductInfo(product_id=good_object['id'],
                                           company_id=supplier.id,
                                           name=good_object['model'],
                                           quantity=good_object['quantity'],
                                           price=good_object['price'],
                                           price_rrc=good_object['price_rrc'])
            else:
                # Если информация по продукту есть - обновляем её
                product_info = ProductInfo(id=existing_prod_info[0].id,
                                           product_id=good_object['id'],
                                           company_id=supplier.id,
                                           name=good_object['model'],
                                           quantity=good_object['quantity'],
                                           price=good_object['price'],
                                           price_rrc=good_object['price_rrc'])
            product_info.save()

            # Загружаем информацию о параметрах продукта
            for parameter_name, parameter_value in (
                    good_object['parameters'].items()):
                existing_parameter = list(Parameter.objects.filter(
                    name=parameter_name))
                if existing_parameter == []:
                    parameter = Parameter(name=parameter_name)
                    parameter.save()
                    product_parameter = ProductParameter(
                        product_info_id=product_info.id,
                        parameter_id=parameter.id,
                        value=parameter_value)
                else:
                    product_parameter = ProductParameter(
                        product_info_id=product_info.id,
                        parameter_id=existing_parameter[0].id,
                        value=parameter_value)
                product_parameter.save()

        return JsonResponse({'Status': True,
                             'Message': f'Loading price of '
                                        f'{supplier.company_name} '
                                        f'completed successfully'})


    def get(self, request, *args, **kwargs):
        return JsonResponse({'Status': False,
                             'Errors': 'Dump price procedure stopper'})