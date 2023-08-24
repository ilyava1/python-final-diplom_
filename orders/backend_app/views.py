from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import (User, Order, Company, Contact, Product, ProductInfo,
                     ProductParameter, OrderItem, ORDER_STATES,
                     CONTACT_TYPE_CHOICES)
from .serializers import (ProductSerializer, ProductInfoSerializer,
                          CompanySerializer, UserSerializer,
                          ContactSerializer, ProductParameterSerializer,
                          OrderSerializer, OrderItemSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


def is_product_id_exists(product_id, order_id=None):
    try:
        int(product_id)
    except:
        return {'Status': False, 'Error': 'Product ID must be num',
                'status_code': 400}
    if int(product_id) < 1:
        return {'Status': False, 'Error': 'Product ID must be greater than 0',
                'status_code': 400}
    else:
        try:
            product = Product.objects.get(id=product_id)
        except:
            return {'Status': False,
                    'Error': f'Product with id={product_id} does not exist',
                    'status_code': 400}
        if order_id != None:
            try:
                order_item = OrderItem.objects.get(product=product_id,
                                                   order=order_id)
            except:
                return {'Status': False,
                        'Error': f'Product with id={product_id} '
                                 f'does not exist',
                        'status_code': 400}
            return order_item
        else:
            return product


def is_company_id_exists(company_id, product_id=None, order_id=None):
    try:
        int(company_id)
    except:
        return {'Status': False, 'Error': 'Company ID must be num',
                'status_code': 400}
    if int(company_id) < 1:
        return {'Status': False, 'Error': 'Company ID must be greater than 0',
                'status_code': 400}
    else:
        try:
            company = Company.objects.get(id=company_id)
        except:
            return {'Status': False,
                    'Error': f'There is no such company ID {company_id}',
                    'status_code': 400}
        if order_id != None and product_id != None:
            try:
                order_item = OrderItem.objects.get(product=product_id,
                                                   order=order_id,
                                                   company=company_id)
            except:
                return {'Status': False,
                        'Error': f'Company with id={company_id} '
                                 f'does not exist',
                        'status_code': 400}
            return order_item
        else:
            return company


def is_quantity_exists(product_id, company_id, quantity):
    try:
        сurrent_product_info = ProductInfo.objects.get(product=product_id,
                                                       company=company_id)
    except:
        return {'Status': False,
                    'Error': f'Wrong product or company ID',
                    'status_code': 400}
    if int(quantity):
        if int(quantity) > 0:
            if сurrent_product_info.quantity < int(quantity):
                return {'Status': False,
                        'Error': f'There is no enought quantyty to satisfy '
                                 f' your request. Current balance for'
                                 f' company id={company_id} '
                                 f'is {сurrent_product_info.quantity} pieces',
                    'status_code': 400}
        else:
            return {'Status': False,
                    'Error': f'Quantity must to be greater than zero',
                    'status_code': 400}
    else:
        return {'Status': False, 'Error': f'Quantity must to be NUM',
                'status_code': 400}

    return сurrent_product_info


def is_user_order_exists(request, order_id=None):
    сurrent_user_order = None
    if order_id == None:
        try:
            сurrent_user_order = Order.objects.get(user_id=request.user.id,
                                                   status='basket')
        except:
            order_id = None
    else:
        try:
            сurrent_user_order = Order.objects.get(user=request.user.id,
                                                   id=order_id,
                                                   status='basket')
        except:
            order_id = None
    if сurrent_user_order:
        order_id = сurrent_user_order.id
    return order_id


def is_same_product_item_exists(data_for_order_item):
    try:
        same_product_item = OrderItem.objects.get(
            order=data_for_order_item['order'],
            product=data_for_order_item['product'],
            company=data_for_order_item['company']
        )
    except:
        same_product_item = None

    return same_product_item


def calc_order_price (order_id):
    # Отбираем и сохраняем в словаре данные по позициям ордера
    try:
        order_items = OrderItem.objects.filter(order=order_id)
    except:
        order_price = {'Status': False,
                'Error': f'Fault during getting order items attempt',
                'status_code': 500}
        return order_price

    # Проходим по позициям ордера и высчитываем стоимость за количество
    order_price = 0
    for item in order_items:
        product_id = item.product
        product_info = ProductInfo.objects.get(product=product_id)
        order_price += product_info.price * item.quantity

    return order_price


class RegisterAccount(APIView):
    """
    Класс для регистрации покупателей
    """

    def post(self, request, *args, **kwargs):
        # Сначала проверяем что все необходимые данные есть в запросе
        if not {'first_name', 'last_name', 'middle_name', 'username', 'email',
            'password', 'position', 'phone', 'company_name',
            'adress'}.issubset(request.data):
            return JsonResponse({'Status': 'Registration IS NOT allowed',
                                 'Detailes': 'Following fields are required:'
                                             ' first_name, last_name, '
                                             'middle_name, username, email, '
                                             'password, position, phone, '
                                             'company_name'}, status=400)
        # и что не одно поле не содержит пустую строку
        exceptions = []
        for field in request.data:
            if field == '':
                exceptions.append(field)
        if exceptions:
            return JsonResponse({'Status': 'Registration IS NOT allowed',
                                 'Detailes': f'{exceptions} field(s) '
                                             f'required'}, status=400)

        # Проверяем есть ли в базе данных компания с именем,
        # указанным в запросе. Если компании нет в базе, регистрация запрещена
        exist_company = Company.objects.filter(
                                company_name=request.data['company_name'])
        if exist_company.exists() == False:
            info_str = f'Error! Company {request.data["company_name"]} ' \
                  f'does not exist in the database yet. ' \
                  f'Before user registration you should ' \
                  f'register company first.' \
                  f'Сontact the administrator.'
            return JsonResponse({'Status': 'Registration IS NOT allowed',
                                 'Detailes': info_str}, status=400)

        # Пользователя не проверяем, есть он или нет в базе -
        # это не важно для регистрации контакта

        # Далее проверяем контакт
        # Новый контакт не создается только в том случае если контакт
        # с такой парой (user - company) уже существует
        exist_user = User.objects.filter(email=request.data['email'])
        if exist_user:
            if Contact.objects.filter(user=exist_user[0].id,
                                      company=exist_company[0].id
                                      ).exists() == True:
                info_str = f'Contact with pair ' \
                           f'({request.data["email"]}' \
                           f' + {request.data["company_name"]}) ' \
                           f'already exists in the database.'
                return JsonResponse({'Status': 'Registration IS NOT allowed',
                                     'Detailes': info_str}, status=400)


        # Если проверки компании и пользователя пройдены
        # (contact_save_ready_status = True), то сохраняем новые объекты
        input_data = request.data

        # Создаем компанию если она не существует
        if exist_company.exists() == False:
            company_serializer = CompanySerializer(data=request.data)
            if company_serializer.is_valid():
                try:
                    new_company = company_serializer.save()
                except:
                    return JsonResponse({'Status': False,
                                         'Error': 'company_serializer.save '
                                                  'method fault'})
                input_data['company'] = new_company.id
            else:
                return JsonResponse({'Status': False,
                                 'Error': company_serializer.errors})
        else:
            input_data['company'] = exist_company[0].id

        # Создаем пользователя если он не сущетвует
        if exist_user.exists() == False:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                try:
                    new_user = user_serializer.save()
                except:
                    return JsonResponse({'Status': False,
                                         'Error': 'user_serializer.save '
                                                  'method fault'})
                if new_user:
                    new_user.set_password(request.data['password'])
                    new_user.save()
                    input_data['user'] = new_user.id
            else:
                return JsonResponse({'Status': False,
                                 'Error': user_serializer.errors})
        else:
            input_data['user'] = exist_user[0].id

        # Сохраняем контакт
        contact_serializer = ContactSerializer(data=input_data)
        if contact_serializer.is_valid():
            try:
                new_contact = contact_serializer.save()
            except:
                return JsonResponse({'Status': False,
                                     'Error': 'contact_serializer.save '
                                              'method fault'})
            status_dict = {'Status': True,
                   'Detailes': f'Registration of the new contact '
                               f'(id={new_contact.id}, '
                               f'user_name={new_contact.user.username}, '
                               f'company={new_contact.company.company_name}) '
                               f'completed successfully.'}
            return JsonResponse(status_dict, status=200)
        else:
            return JsonResponse({'Status': False,
                                 'Detailes': contact_serializer.errors})

#-----------------------------------------------------------------------------


class ProductCatalog(APIView):
    """
    Класс для просмотра каталога продуктов
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)


class ProductCard(APIView):
    """
    Класс для просмотра карточки продукта
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        product_id = kwargs['product_id']
        product = is_product_id_exists(product_id)
        if type(product) == dict:
            return Response({'Status': product['Status'],
                             'Error': product['Error']},
                     status=product['status_code'])


        serializer = ProductSerializer(product)
        product_card = {}
        product_card['product'] = serializer.data

        product_info = ProductInfo.objects.get(product_id=product_id)
        if not product_info:
            product_card['product_info'] = f'There is no product info '\
                                           f'for product ID {product_id}'
        else:
            serializer = ProductInfoSerializer(product_info)
            product_card['product_info'] = serializer.data

            product_params = ProductParameter.objects.filter(product_info=
                                                             product_info)
            if not product_params:
                product_card['product_params'] = f'There is no product params'\
                                                 f' for product ID=' \
                                                 f'{product_id}'
            else:
                serializer = ProductParameterSerializer(product_params,
                                                        many=True)
                product_card['product_info']['product_params'] = (
                    serializer.data)

        return Response(product_card)


class AddToOrder(APIView):
    """
    Класс для добавления продукта в заказ
    """
    def post(self, request, *args, **kwargs):
        # Проверка пользователя на авторизацию
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        product_id = kwargs['product_id']
        # Проверка id продукта на существование
        product = is_product_id_exists(product_id)
        if type(product) == dict:
            return Response({'Status': product['Status'],
                             'Error': product['Error']},
                            status=product['status_code'])

        company_id = kwargs['company_id']
        # Проверка id компании на существование
        company = is_company_id_exists(company_id)
        if type(company) == dict:
            return Response({'Status': company['Status'],
                             'Error': company['Error']},
                            status=company['status_code'])

        # Проверка наличия запрошенного количества продукта у компании
        quantity = kwargs['quantity']
        сurrent_product_info = is_quantity_exists(product_id, company_id,
                                                  quantity)
        if type(сurrent_product_info) == dict:
            return Response({'Status': сurrent_product_info['Status'],
                             'Error': сurrent_product_info['Error']},
                            status=сurrent_product_info['status_code'])

        # Проверка наличия у данного пользователя заказа в статусе 'basket'
        # т.е. такого в который можно дабавить позицию
        order_id = is_user_order_exists(request)

        # Если заказа данного пользователя в статусе 'basket' нет в базе
        # - создаем заказ
        if order_id == None:
            data_for_order = {'user': request.user.id}
            order_serializer = OrderSerializer(data=data_for_order)
            if order_serializer.is_valid():
                try:
                    order = order_serializer.save()
                except:
                    return Response({'Status': False,
                                     'Detailes': order_serializer.errors},
                                    status=500)

            data_for_order_item = {'order': order.id, 'product': product_id,
                              'company': company_id, 'quantity': quantity}
        else:
            # Если заказ уже есть, то подставляем его id в набор данных для
            # создания позиции заказа
            data_for_order_item = {'order': order_id, 'product': product_id,
                                   'company': company_id,
                                   'quantity': quantity}
        # Прежде чем создавать позицию заказа проверяем нет ли в заказе
        # того же продукта той же компании
        same_product_item = is_same_product_item_exists(data_for_order_item)
        # Если такой позиции в заказе нет, то создаем новую
        if same_product_item == None:
            order_item_serializer = OrderItemSerializer(
                data=data_for_order_item)
            if order_item_serializer.is_valid():
                try:
                    order_item = order_item_serializer.save()
                except:
                    return Response({'Status': False, 'Detailes': f'Error '
                                    f'order_item_serializer.save method'},
                                    status=500)
            else:
                return Response({'Status': False, 'Detailes':
                                    order_item_serializer.errors},
                                status=500)
        # Если такая позиция уже есть в заказе, то только плюсуем количество
        else:
            new_item_quantity = int(same_product_item.quantity) + int(quantity)
            order_item_serializer = OrderItemSerializer(
                same_product_item,
                data={'quantity': new_item_quantity})
            if order_item_serializer.is_valid():
                # И обновляем строчку заказа новым количеством
                try:
                    order_item_serializer.save()
                except:
                    return Response({'Status': False, 'Detailes': f'Error '
                                    f'order_item_serializer.save method'},
                                    status=500)
            else:
                return Response({'Status': False, 'Detailes':
                    order_item_serializer.errors}, status=500)

        # Далее реализуем логику по уменьшению кол-ва продукта компании в базе

        new_product_info_quantity = сurrent_product_info.quantity - (
            int(quantity))
        data = {'name': сurrent_product_info.name,
                'price': сurrent_product_info.price,
                'price_rrc': сurrent_product_info.price_rrc,
                'quantity': new_product_info_quantity}
        product_info_serializer = ProductInfoSerializer(сurrent_product_info,
                                                        data=data)
        if product_info_serializer.is_valid():
            try:
                product_info = product_info_serializer.save()
            except:
                return Response({'Status': False, 'Detailes': f'Error '
                                f'product_info_serializer.save method'},
                                status=500)
        else:
            return Response({'Status': False,
                             'Detailes': product_info_serializer.errors},
                            status=500)

        return Response({'Status': 'OK',
                         'Detailes': f'Product added to order '
                                     f'id={data_for_order_item["order"]}'},
                        status=200)

class DelFromOrder(APIView):
    """
    Класс для удаления n-го количества продукта из заказа
    """
    def delete(self, request, *args, **kwargs):
        # Проверка пользователя на авторизацию
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        # Проверка id заказа на существование (ищем заказы в статусе 'basket')
        order_id = kwargs['order_id']
        order_id = is_user_order_exists(request, order_id)
        if not order_id:
            return JsonResponse({'Status': False,
                                 'Error': 'Wrong order ID'}, status=400)

        product_id = kwargs['product_id']
        # Проверка id продукта на существование в найденном заказе
        product = is_product_id_exists(product_id, order_id)
        if type(product) == dict:
            return Response({'Status': product['Status'],
                             'Error': product['Error']},
                            status=product['status_code'])

        company_id = kwargs['company_id']
        # Проверка id компании на существование в найденном заказе
        order_item = is_company_id_exists(company_id, product_id, order_id)
        if type(order_item) == dict:
            return Response({'Status': order_item['Status'],
                             'Error': order_item['Error']},
                            status=order_item['status_code'])

        # Проверка того, что в заказе есть нужное количество продукта
        quantity = kwargs['quantity']
        if order_item.quantity >= int(quantity):
            new_quantity = order_item.quantity - int(quantity)
        else:
            return Response({'Status': False,
                                 'Error': f'Quantity in request (={quantity})'
                                          f' is greater then quantity in order'
                                          f' item (={order_item.quantity})'},
                                status=400)

        # Обновляем строчку заказа новым количеством продукта
        order_item_serializer = OrderItemSerializer(
            order_item, data={'quantity': new_quantity})
        if order_item_serializer.is_valid():
            try:
                order_item_serializer.save()
            except:
                return Response({'Status': False,
                                 'Error': f'Order_item_serializer '
                                          f'save method'},
                                status=500)
        else:
            return Response({'Status': False,
                             'Error': order_item_serializer.errors},
                            status=500)

        # Далее реализуем логику по увеличению кол-ва продукта компании в базе
        try:
            сurrent_product_info = ProductInfo.objects.get(company=company_id,
                                                           product=product_id)
        except:
            Response({'Status': False,
                      'Error': 'Fault during getting ProductInfo object'},
                     status=500)
        new_product_info_quantity = сurrent_product_info.quantity + (
            int(quantity))
        data = {'name': сurrent_product_info.name,
                'price': сurrent_product_info.price,
                'price_rrc': сurrent_product_info.price_rrc,
                'quantity': new_product_info_quantity}
        product_info_serializer = ProductInfoSerializer(сurrent_product_info,
                                                        data=data)
        if product_info_serializer.is_valid():
            try:
                product_info_serializer.save()
            except:
                return Response({'Status': False,
                                 'Detailes': f'Error during '
                                             f'product_info_serializer.save'
                                             f' method'},
                                status=500)
        else:
            return Response({'Status': False,
                             'Error': product_info_serializer.errors},
                            status=500)

        return Response({'Status': True,
                         'Detailes': f'Quantity in order item '
                                     f'id={order_item.id} in order '
                                     f'id={order_id} reduced by {quantity}'
                                     f' pieces and it is now {new_quantity}'},
                        status=200)

class ViewOrder(APIView):
    """
    Класс для просмотра заказа
    """
    def get(self, request, *args, **kwargs):
        # Проверка пользователя на авторизацию
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        # Проверяем корректен ли номер заказа
        order_id = kwargs['order_id']
        try:
            order = Order.objects.get(id=order_id)
        except:
            return Response({'Status': False,
                             'Error': f'Wrong order id={order_id}.'},
                            status=400)

        # Далее производится расчет стоимости позиции и заказа вцелом
        # Сохраняем в словаре данные по ордеру
        order_serializer = OrderSerializer(order)
        order_data = {}
        order_data['order'] = order_serializer.data

        # Отбираем и сохраняем в словаре данные по позициям ордера
        try:
            order_items = OrderItem.objects.filter(order=order_id)
        except:
            Response({'Status': False,
                      'Error': f'Fault during getting order items attempt'},
                     status=500)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        order_data['order_items'] = order_item_serializer.data

        # Проходим по позициям ордера и высчитываем стоимость за количество
        order_price = 0
        item_price = 0
        i = 0
        for item in order_items:
            product_id = item.product
            product_info = ProductInfo.objects.get(product=product_id)
            order_price += product_info.price * item.quantity
            item_price += product_info.price * item.quantity
            order_data['order_items'][i]['price for quantity'] = item_price
            item_price = 0
            i += 1

        order_data['total price'] = order_price

        return Response(order_data)


class ViewOrderHistory(APIView):
    """
    Класс для просмотра истории заказов
    """
    def get(self, request, *args, **kwargs):
        # Проверка пользователя на авторизацию
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        orders = Order.objects.filter(user=request.user.id)
        all_orders = []
        for order in orders:
            order_serializer = OrderSerializer(order)
            current_order = order_serializer.data
            current_order['price for quantity'] = calc_order_price (order.id)
            all_orders.append(current_order)
        return Response(all_orders)


class ChangeOrderStatus(APIView):
    """
    Класс для изменения статуса заказов
    """
    def post(self, request, *args, **kwargs):
        # Проверка пользователя на авторизацию
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=401)

        # Проверям ордер на существование
        order_id = kwargs['order_id']
        try:
            order = Order.objects.get(id=order_id)
        except:
            return Response({'Status': False,
                             'Error': f'Wrong order id={order_id}.'},
                             status=400)

        # Поверяем корректность статуса в запросе
        order_status = kwargs['order_status']
        for status in ORDER_STATES:
            fl = 0
            if order_status in status:
                fl = 1
                break
        if fl == 0:
            return Response({'Status': False,
                             'Error': f'Wrong order status={order_status}.'},
                             status=400)

        # Выясняем представителем какой компании является пользователь,
        # от этого будет зависеть какие статусы сможет присваивать
        # пользователь заказу

        contact = Contact.objects.filter(user=request.user.id)
        if contact.exists():
            company = Company.objects.get(id=contact[0].company.id)

        # Проверям яляется ли пользователь из запроса создателем заказа,
        # представляет магазин и только ли разрешенные статусы пытается применить

        if ((order.user.id == request.user.id) and
                (company.type in CONTACT_TYPE_CHOICES[1])):
            # Если да, то пользователь - покупатель и имеет право на установку
            # статусов basket, new, canceled
            if (order_status in ORDER_STATES[0]) \
                    or (order_status in ORDER_STATES[1]) \
                    or (order_status in ORDER_STATES[6]):
                if not (order.status == 'delivered'
                        and order_status == 'canceled'):
                    data = {'status': order_status}
                    order_serializer = OrderSerializer(order, data=data)
                    if order_serializer.is_valid():
                        order_serializer.save()
                    else:
                        return Response({'Status': False,
                                     'Error': {order_serializer.errors}},
                                    status=500)
                else:
                    return Response({'Status': False,
                                     'Error': f'Delivered order can not '
                                              f'be canceled'},
                                    status=400)
            else:
                return Response({'Status': False,
                                 'Error': f'You cant assign '
                                          f'status={order_status}.'},
                                 status=400)
        elif company.type in CONTACT_TYPE_CHOICES[0]:
            # Иначе проверяем что пользователь - менеджер по продажам и имеет право на
            # установку статусов confirmed, assembled, sent, delivered
            if (order_status in ORDER_STATES[2]) \
                or (order_status in ORDER_STATES[3]) \
                or (order_status in ORDER_STATES[4]) \
                or (order_status in ORDER_STATES[5]):
                if not order.status == 'canceled':
                    data = {'status': order_status}
                    order_serializer = OrderSerializer(order, data=data)
                    if order_serializer.is_valid():
                        order_serializer.save()
                    else:
                        return Response({'Status': False,
                                     'Error': {order_serializer.errors}},
                                    status=500)
                else:
                    return Response({'Status': False,
                                     'Error': f'Canceled orders can not '
                                              f'be moved to a different '
                                              f'status by the supplier'},
                                    status=400)
            else:
                return Response({'Status': False,
                                 'Error': f'You cant assign '
                                          f'status={order_status}.'},
                                status=400)

        else:
            return Response({'Status': False,
                             'Error': f'You cant assign '
                                      f'status for tis order.'},
                            status=400)

        return Response({'Status': True,
                         'Detales': f'For order id={order_id}'
                                    f' assigned status={order_status}.'},
                          status=200)

